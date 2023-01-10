# SRVE - Crypto for the People
SRVE is an open-source cryptocurrency exchange powered by LOTS of exchanges! Learn how we work below!

[Discord](https://discord.gg/bwRwdbADnH) | [Website (Soon)](#)

## How it works
SRVE uses other (no KYC/instant/DEX) exchange's APIs to preform requests on your behalf for privacy or ease-of-use purposes. Here's how a transaction works!

You go to SRVE and input an amount -> We return a recieve price for your pair -> You accept the offer -> We use FixedFloat's API (for now) to get a trade ready for you -> We display the amounts and addresses -> We keep you posted along the way about the status of your trade!

And it's all baked into a clean UI free from distractions and ads! We're commission free (except for partner exchange fees), and (of course) totally free to use, with no sign up required!

## Fixedfloat API
The fixedfloat API (repaired and edited) will be published in the coming future (as the project has been deleted on GitHub), and has been archived and edited to work with my program. If you plan on self-hosting this, please send me a message on Discord (XNO#5560) to obtain the edited copy (or if you just want the archive)!

This module, though, is still avaliable to install on pip!

## Self Hosting
Self hosting is totally possible! Here's how to do it!

1. Install Python
2. Install flask and fixedfloat from pip
3. Edit main.py ```lines 12 and 13``` with your FixedFloat API key (get this from [fixedfloat.com/apikey](https://fixedfloat.com/apikey))
3. Type ```flask run``` to spin up a development server for personal use
4. Navigate to ```http://127.0.0.1/``` to use the exchange!

## Status
*Status:* **Code Completed for Desktop!**
*In Progress/Next Update:* **Mobile-friendly UI**

SRVE's first release for code is completed, and we're ready to launch our services (once a domain is aquired)!

## Our Accounts/Threads
- BitcoinTalk ([Profle](https://bitcointalk.org/index.php?action=profile;u=3527144)) - [Announcement Thread](https://bitcointalk.org/index.php?topic=5433409)
