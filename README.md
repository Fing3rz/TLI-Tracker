# FurTorch

My take on the English revamp of FurTorch.

This is a Standalone version, which means we don't use a connection to the FurTorch devs servers for price updates.

It was first translated and fixed with AI by another Dev (see main repository I forked from).

I'm now fixing every single translation with no AI usage, as well as adding new features.

# New Features from this Fork:

## UI Related

- Coloured text for clearer visualization of gains and losses/consumption (Green/Red)
- Proper translation of every common item in the game (Generic Loot, Compasses, Map Material, Fluorescent Memories, Corrosion Material)

  ## Price Updates in real time

- - Price Checking in the AH properly updates prices on the Tracker in real time, no need to reload!

## Code Structure + Standalone Version

- No more usage of the main repositories server to update prices -> this was causing a lot of connection issues and thus prices weren't updating correctly, this is now a Standalone version.
- Reduced dependency on Chinese AI translation and price mapping -> easier for new devs to hop in and develop new features

## Installation

1. Ensure you have Python installed (version 3.6 or higher, preferably only up to 3.10 for fewer errors)
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the English version of the application:
   ```
   python index.py
   ```
