/**
 * @file main.c
 * @brief Main program for controlling devices via MQTT and sensor readings.
 * This program is responsible for controlling an IoT device that performs temperature and humidity measurements
 * using sensors and sends the data to an MQTT server for processing and visualization.
 */
#include <stdio.h> //for basic printf commands
#include <string.h> //for handling strings
#include <stdbool.h>
#include "freertos/FreeRTOS.h" //for delay,mutexs,semphrs rtos operations
#include "esp_system.h" //esp_init funtions esp_err_t 
#include "esp_wifi.h" //esp_wifi_init functions and wifi operations
#include "esp_log.h" //for showing logs
#include "esp_event.h" //for wifi event
#include "nvs_flash.h" //non volatile storage
#include "lwip/err.h" //light weight ip packets error handling
#include "lwip/sys.h" //system applications for light weight ip apps
#include "mqtt_client.h" //Mqt


//GPIO DRIVER
#include "driver/gpio.h"
//ADC ONE shot include
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_adc/adc_oneshot.h"
#include "esp_adc/adc_cali.h"
#include "esp_adc/adc_cali.h"
#include "driver/ledc.h"

#define EXAMPLE_ADC_UNIT        ADC_UNIT_1
#define EXAMPLE_ADC_ATTEN       ADC_ATTEN_DB_12
#define EXAMPLE_ADC_CHAN0       ADC_CHANNEL_6 //GPIO 34
#define EXAMPLE_ADC_CHAN1       ADC_CHANNEL_7 //GPIO 35

#define LED_OUTPUT GPIO_NUM_4

static int adc_raw[2]; //lectura sensorar
static int freq = 2000; //freq lectura
static adc_oneshot_unit_handle_t adc_handle;
static adc_cali_handle_t  cali_handle;

static bool disconnected =1; //Wifi disconnect flag
static bool connected_mqtt_broker = false; //broker state
static int retry_num = 0;
static esp_mqtt_client_handle_t client;

static int led_state=0; //state of led


static void wifi_event_handler(void *event_handler_arg,esp_event_base_t event_base, int32_t event_id,void *event_data){
  /**
   * @brief WiFi event handler. Controls the WiFi connection state.
   */
  switch(event_id){
  case WIFI_EVENT_STA_START:
    printf("CONECTANT A WIFI ...\n");
    break;

  case WIFI_EVENT_STA_CONNECTED:
    printf("WIFI CONNECTAT\n");
    disconnected=0;
  
    break;
    
  case WIFI_EVENT_STA_DISCONNECTED:
    printf("Connexió perduda \n");
    if(retry_num<100){esp_wifi_connect();retry_num++;printf("Intentant reconectar...\n");}
    disconnected=1;
    break;
  case IP_EVENT_STA_GOT_IP:
    printf("OBTINGUT IP DEL WIFI \n");
  }
}




void wifi_connection(void){
  /**
 * @brief Initializes the WiFi connection.
 */
  esp_netif_init();
  esp_event_loop_create_default();
  esp_netif_create_default_wifi_sta();
  
  wifi_init_config_t wifi_initiation = WIFI_INIT_CONFIG_DEFAULT(); //Creació configuració wifi ini amb default
  esp_wifi_init(&wifi_initiation);  //Inicialització default
  esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, wifi_event_handler, NULL); //Gestor d'events pel wifi 
  esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, wifi_event_handler, NULL); //Gestor d'events per IP's
  wifi_config_t wifi_configuration ={ //Configuració Wifi
    .sta= {
      .ssid = "MiFibra-5FA2",
      .password= "4kz2JmRu",
      .scan_method=WIFI_ALL_CHANNEL_SCAN,
    },
  };
  esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_configuration); //Aplicat condifuració
  esp_wifi_start(); //Inici connexió
  esp_wifi_set_mode(WIFI_MODE_STA); //mode wifi STA és conecta a un punt d'accés
  esp_wifi_connect();
}

//MQTT CONFIGURACIÓ

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data){
  /**
   * @brief MQTT event handler. Controls the connection and interactions with the MQTT server.
 */
  esp_mqtt_event_handle_t event = event_data;
  esp_mqtt_client_handle_t client = event->client;
  //int msg_id;
  switch ((esp_mqtt_event_id_t)event_id){
  case MQTT_EVENT_CONNECTED:
    esp_mqtt_client_subscribe(client, "led_act", 1);
    connected_mqtt_broker = true; //broker connected
    break;
  case MQTT_EVENT_DISCONNECTED:
    connected_mqtt_broker = false;//broker state off
    printf("MQTT desconectat \n");
    break;

  case MQTT_EVENT_SUBSCRIBED:
    printf("Suscribit, msg_id=%d\n",event->msg_id);
    break;

  case MQTT_EVENT_UNSUBSCRIBED:
    printf("desuscribit, msg_id=%d\n", event->msg_id);
    break;
  case MQTT_EVENT_PUBLISHED:
    printf("publicat, msg_id=%d\n", event->msg_id);
    break;
  case MQTT_EVENT_DATA:
    printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
    printf("DATA=%.*s\r\n", event->data_len, event->data);
    if (strncmp(event->data, "1", event->data_len) == 0) {
      gpio_set_level(LED_OUTPUT, 1);
      led_state = 1;
      printf("POWERN ON\n");
    } else {
      gpio_set_level(LED_OUTPUT, 0);
      led_state = 0;
      printf("POWERN OFF\n");
    }
    printf("event data \n");
    break;
  case MQTT_EVENT_ERROR:
    printf("Error \n");
    break;
  default:
    printf("Un altre event id:%d\n",event->msg_id);
    break;
  }
}

static void mqtt_app_start(void){
  /**
   * @brief Starts the MQTT application.
 */
  esp_mqtt_client_config_t mqtt_cfg = {
    .broker.address.uri = "mqtt://192.168.1.88", //Configuració broker mqtt
  };
  client=esp_mqtt_client_init(&mqtt_cfg);
  esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, client);
  esp_mqtt_client_start(client);    
}

void config_adc(void){ //conf ADC input
  /**
   * @brief Configures the ADC (Analog-to-Digital Converter) for sensor readings.
 */
  adc_oneshot_unit_init_cfg_t init_config = {
    .unit_id = EXAMPLE_ADC_UNIT,
  };

  ESP_ERROR_CHECK(adc_oneshot_new_unit(&init_config, &adc_handle));
  adc_oneshot_chan_cfg_t config = {
    .bitwidth = ADC_BITWIDTH_DEFAULT,
    .atten = EXAMPLE_ADC_ATTEN,
  };
  ESP_ERROR_CHECK(adc_oneshot_config_channel(adc_handle, EXAMPLE_ADC_CHAN0, &config));
  ESP_ERROR_CHECK(adc_oneshot_config_channel(adc_handle, EXAMPLE_ADC_CHAN1, &config));
  adc_cali_line_fitting_config_t cali_config = {
    .unit_id = EXAMPLE_ADC_UNIT,
    .atten = EXAMPLE_ADC_ATTEN,
    .bitwidth = ADC_BITWIDTH_DEFAULT,
  };
  ESP_ERROR_CHECK(adc_cali_create_scheme_line_fitting(&cali_config, &cali_handle));

}

void config_output(void){
  
  /**
   * @brief Configures the GPIO output for device control.
   */
  gpio_config_t io_conf = {
    .pin_bit_mask = (1ULL << LED_OUTPUT), 
    .mode = GPIO_MODE_OUTPUT,               
    .pull_up_en = GPIO_PULLUP_DISABLE,      
    .pull_down_en = GPIO_PULLDOWN_DISABLE,  
    .intr_type = GPIO_INTR_DISABLE          
  };
  gpio_config(&io_conf);
}
float generar_numero(void) {
    return rand() % 31 + 50; // Genera un número aleatorio entre 50 y 80
}


void app_main(void)
{
  
  /**
 * @brief Main function of the application.
 */
  config_adc();
  config_output();
  nvs_flash_init(); //Permet guardar la configuració
  wifi_connection();
  gpio_set_level(LED_OUTPUT, 0); //ini led to 0
  while(disconnected){
    printf("Connecting... \n");
    vTaskDelay(pdMS_TO_TICKS(3000));
  }
  mqtt_app_start();
  while(1){
    
    if (connected_mqtt_broker){
      char buffer[10];
      int volt;
      float hum;
      
      
      adc_oneshot_read(adc_handle, EXAMPLE_ADC_CHAN0, &adc_raw[0]);
      
      adc_cali_raw_to_voltage(cali_handle, adc_raw[0], &volt); // raw to voltatge
     
      float temp=((float)volt/1000-0.5)/0.01-4;
      sprintf(buffer,"0,%.1f",temp);
      esp_mqtt_client_publish(client,"temperature_assi",buffer,0,1,0);
      adc_oneshot_read(adc_handle, EXAMPLE_ADC_CHAN1, &adc_raw[1]);
      hum = generar_numero();
      sprintf(buffer,"1,%.1f",hum);
      esp_mqtt_client_publish(client,"humitat_assi",buffer,0,1,0);
      sprintf(buffer,"2,%d",led_state);
      esp_mqtt_client_publish(client,"led_assi",buffer,0,1,0);
      vTaskDelay(pdMS_TO_TICKS(freq));
    }
    else{
      printf("Looking for MQTT Broker...\n");
      vTaskDelay(pdMS_TO_TICKS(3000));
    }
  }
}

