// Define relay pins
const int relayPins[] = {2, 3, 4, 5, 6}; // Pins D2 to D6
const int numRelays = 5; // Number of relays
const int relayOnDuration = 500; // Duration to turn on the relay for the poofer
const int relayOffDuration = 100; // inter poofer interval (in milliseconds) should be typically low 
const int pauseDuration = 10000; // time between sequences - refractory time

// Define relay sequences
const int sequence1[] = {4, 3, 2, 1, 5}; // Sequence for 'a'
const int sequence2[] = {1, 5, 4, 3, 2}; // Sequence for 'b'
const int sequence3[] = {2, 4, 1, 5, 3}; // Sequence for 'c'
const int sequence4[] = {5, 1, 3, 2, 4}; // Sequence for 'd'

// Variable to store the current sequence
const int* currentSequence = sequence1;

void setup() {
  // Initialize each relay pin as an output
  for (int i = 0; i < numRelays; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], LOW); // Ensure relays are off initially
  }

  // Start serial communication
  Serial.begin(9600); // Adjust baud rate as needed
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming byte

    // Select the sequence based on the received command
    switch (command) {
      case 'a':
        currentSequence = sequence1;
        break;
      case 'b':
        currentSequence = sequence2;
        break;
      case 'c':
        currentSequence = sequence3;
        break;
      case 'd':
        currentSequence = sequence4;
        break;
      default:
        return; // Ignore invalid commands
    }

    // Activate relays in the chosen sequence
    for (int i = 0; i < numRelays; i++) {
      int relayIndex = currentSequence[i] - 1; // Calculate index based on the sequence (1-based index)
      digitalWrite(relayPins[relayIndex], HIGH); // Turn on relay
      delay(relayOnDuration); // Wait for relayOnDuration
      digitalWrite(relayPins[relayIndex], LOW); // Turn off relay
      delay(relayOffDuration); // Wait for relayOffDuration before the next relay (inter poofer interval)
    }

    // Pause for pauseDuration before starting the sequence again
    delay(pauseDuration);
  }
}
