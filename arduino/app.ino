#include <ESP8266WiFi.h>

//SSID of your network
char ssid[] = "ichbins"; //SSID of your Wi-Fi router
char pass[] = "210892c270894220"; //Password of your Wi-Fi router
char plantName[] = "plant-1";

WiFiServer server(80);

void setup()
{
  Serial.begin(9600);
  Serial.print("Connecting to...");
  Serial.println(ssid);

  WiFi.hostname(plantName);
  WiFi.begin(ssid, pass);

  while (! WiFi.isConnected()) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Wi-Fi connected successfully");

  server.begin();
  Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());
}

String prepareJsonResponse()
{
  String jsonResponse =
     String("HTTP/1.1 200 OK\r\n") +
            "Content-Type: application/json\r\n" +
            "Connection: close\r\n" +  // the connection will be closed after completion of the response
            "Refresh: 5\r\n" +  // refresh the page automatically every 5 sec
            "\r\n" +
            "{" +
            "\"" + plantName + "\" : " + String(analogRead(A0)) +
            "}" +
            "\r\n";
  return jsonResponse;
}

void loop () {
  WiFiClient client = server.available();
  // wait for a client (web browser) to connect
  if (client)
  {
    Serial.println("\n[Client connected]");
    while (client.connected())
    {
      // read line by line what the client (web browser) is requesting
      if (client.available())
      {
        String line = client.readStringUntil('\r');
        Serial.print(line);
        // wait for end of client's request, that is marked with an empty line
        if (line.length() == 1 && line[0] == '\n')
        {
          client.println(prepareJsonResponse());
          break;
        }
      }
    }
    delay(1); // give the web browser time to receive the data

    // close the connection:
    client.stop();
    Serial.println("[Client disonnected]");
  }
}
