const int ledPin = 13; // Pino do LED

void setup()
{
    pinMode(ledPin, OUTPUT);
    Serial.begin(9600); // A taxa de transmissão deve corresponder à definida no Unity
}

void loop()
{
    if (Serial.available() > 0)
    {
        char receivedChar = Serial.read();
        if (receivedChar == '1')
        {
            digitalWrite(ledPin, HIGH); // Liga o LED
            delay(1000); // Mantém o LED aceso por 1 segundo (opcional)
            digitalWrite(ledPin, LOW); // Desliga o LED
        }
    }
}
