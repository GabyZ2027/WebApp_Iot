#include <stdio.h> //for basic printf commands
#include <string.h> //for handling strings
#include "freertos/FreeRTOS.h" //for delay,mutexs,semphrs rtos operations
#include "esp_system.h" //esp_init funtions esp_err_t 
#include "esp_wifi.h" //esp_wifi_init functions and wifi operations
#include "esp_log.h" //for showing logs
#include "esp_event.h" //for wifi event
#include "nvs_flash.h" //non volatile storage
#include "lwip/err.h" //light weight ip packets error handling
#include "lwip/sys.h" //system applications for light weight ip apps
#include "mqtt_client.h"

static int retry_num = 0;

static void wifi_event_handler(void *event_handler_arg,esp_event_base_t event_base, int32_t event_id,void *event_data){
  switch(event_id){
  case WIFI_EVENT_STA_START:
    printf("CONECTANT A WIFI ...\n");
    break;

  case WIFI_EVENT_STA_CONNECTED:
    printf("WIFI CONNECTAT\n");
    break;
    
  case WIFI_EVENT_STA_DISCONNECTED:
    printf("Connexió perduda \n");
    if(retry_num<5){esp_wifi_connect();retry_num++;printf("Intentant reconectar...\n");}
    break;
  case IP_EVENT_STA_GOT_IP:
    printf("OBTINGUT IP DEL WIFI \n");
  }
}

void wifi_connection(void){
  esp_netif_init();
  esp_event_loop_create_default();
  esp_netif_create_default_wifi_sta();
  
  wifi_init_config_t wifi_initiation = WIFI_INIT_CONFIG_DEFAULT(); //Creació configuració wifi ini amb default
  esp_wifi_init(&wifi_initiation);  //Inicialització default
  esp_event_handler_register(WIFI_EVENT, ESP_EVENT_ANY_ID, wifi_event_handler, NULL); //Gestor d'events pel wifi 
  esp_event_handler_register(IP_EVENT, IP_EVENT_STA_GOT_IP, wifi_event_handler, NULL); //Gestor d'events per IP's
  wifi_config_t wifi_configuration ={ //Configuració Wifi
    .sta= {
      .ssid = "",
      .password= "", 
    },
  };
  esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_configuration); //Aplicat condifuració
  esp_wifi_start(); //Inici connexió
  esp_wifi_set_mode(WIFI_MODE_STA); //mode wifi STA és conecta a un punt d'accés
  esp_wifi_connect();
}

//MQTT CONFIGURACIÓ

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data){ //HANDLER Gestió 
  esp_mqtt_event_handle_t event = event_data;
  esp_mqtt_client_handle_t client = event->client;
  int msg_id;
  switch ((esp_mqtt_event_id_t)event_id){
  case MQTT_EVENT_CONNECTED:
    msg_id = esp_mqtt_client_publish(client,"/topic/prova","Prova enviant dada",0,1,0); //enviar missatge
    printf("Missatge amb ID enviat %d\n",msg_id);
    break;
  case MQTT_EVENT_DISCONNECTED:
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
  esp_mqtt_client_config_t mqtt_cfg = {
    .broker.address.uri = "mqtt://mqtt.eclipseprojects.io", //Configuració broker mqtt
  };
  esp_mqtt_client_handle_t client=esp_mqtt_client_init(&mqtt_cfg);
  esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
  esp_mqtt_client_start(client);
    
}

void app_main(void)
{
  nvs_flash_init(); //Permet guardar la configuració
  wifi_connection();

  vTaskDelay(20000 /portTICK_PERIOD_MS);//Delay per esperar a que es conecti a wifi
  mqtt_app_start();
}