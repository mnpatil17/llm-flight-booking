# Flight Booking

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

To develop, you need to have two tokens:

1. [OpenAI](https://platform.openai.com/account/api-keys) - Create an OpenAI account, and get an API key. Then save it
   in `~/.tokens/openai.token` on your local machine
2. [Duffel](https://app.duffel.com/) - Create an Duffel account, and get an API key. Then save it
   in `~/.tokens/duffel.token` on your local machine

Then, install the following:

1. `pip install openai`
