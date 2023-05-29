# Flight Booking

### Example of existing functionality

```
   What city are you in now?: Chicago, IL
   Where would you like to go?: I'd like to go to Mumbai, on Friday, and I'd like to come back on the following Saturday

   Itinerary | Total Cost: 1117.72 USD
   ORD to BOM
        Flight 1: ZZ 5579  | ORD to BOM | June 02, 2023 at 00:46 to June 03, 2023 at 05:16
   BOM to ORD
        Flight 1: ZZ 5579  | BOM to ORD | June 10, 2023 at 06:58 to June 10, 2023 at 14:28

   Itinerary | Total Cost: 1302.23 USD
   ORD to BOM
        Flight 1: AC 8910  | ORD to YYZ | June 02, 2023 at 15:40 to June 02, 2023 at 18:17
        Flight 2: AC 42    | YYZ to DEL | June 02, 2023 at 20:10 to June 03, 2023 at 20:50
        Flight 3: UK       | DEL to BOM | June 04, 2023 at 09:00 to June 04, 2023 at 11:15

   [...]
```

## Proof-of-Concept

The proof-of-concept is now complete. At this time, we're able to:

1. Convert a natural language query to a set of parameters, using GPT-3.5
2. Query the [Duffel API](https://duffel.com/docs/api/overview/welcome) to get back corresponding flights
3. Print out these flights

#### LLM-layer Functionality & Gaps

The LLM is able to:

1. Understand preferred class of travel
2. Understand dates of travel (outbound and inbound)
3. Understand preferred airlines
4. Return a human-readable error for the prompt

The LLM currently cannot understand:

1. Compose multi-city trips
2. Understand user preferences for price vs. duration
3. Get seat preferences ("Seat 1A", "Aisle")
4. Cannot converse with the user to coax more information

#### Software-layer functionality and gaps

At this point the software-layer is able to:

1. Call the Duffel API and get the flights

It is, however, not able to:

1. Respect airline preferences (this would be a simple filteration)
2. Respect optimize price sensitivity vs. duration vs. airline preferences
3. Do anything after displaying the flights. There's no booking, possible
4. There's no user authentication at this time.

## Development

#### Setup

To develop, you need to have two tokens:

1. [OpenAI](https://platform.openai.com/account/api-keys) - Create an OpenAI account, and get an API key. Then save it
   in `~/.tokens/openai.token` on your local machine
2. [Duffel](https://app.duffel.com/) - Create an Duffel account, and get an API key. Then save it
   in `~/.tokens/duffel.token` on your local machine

Then, install the following:

1. `pip install openai`

#### Development Workflow

Because calls to OpenAI are expensive, in the `main.py` file, we have a boolean flag called `FLIGHT_TESTING_MODE`.
If you turn on testing mode, the script will not make calls to OpenAI; instead it'll output a fake result from the
OpenAI API. This is useful when you're debugging the software-layer (i.e. the interactions with the flights).

To run the end-to-end workflow, set `FLIGHT_TESTING_MODE` to `False`, and run the main section of `main.py` file.
