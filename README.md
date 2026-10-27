# FAST Forward sign-up page (Netlify + SendFox)

A copy of fastforward.crd.co. It uses the same Netlify + SendFox sign-up setup as the Values Cards.
Sign-ups go to SendFox list **618152 ("getfastforward")**.
There's no Amazon link and no LinkedIn link: the only thing a visitor can do is sign up.

## How it works
Form -> POST `/.netlify/functions/subscribe` `{ email, listId: 618152 }` -> SendFox, using `SENDFOX_API_KEY`.
The list ID is set near the top of the script in `index.html` (`LIST_ID`).

## Where the files go
- **New Netlify site (GitHub repo preferred):** put this whole folder at the repo root.
  `netlify/functions/subscribe.js` and `netlify.toml` must sit at the root.
- **Adding to a site that already has `subscribe.js`:** copy only `index.html` and `images/`
  (put them in a sub-folder if you like, e.g. `/fastforward/`). Don't copy the function or `netlify.toml`.
  The existing function takes the list ID from the page.

## One-time Netlify setup (new site only)
Site configuration -> Environment variables -> Key `SENDFOX_API_KEY`, Value = your SendFox token,
tick "Contains secret values". (Common mistake: pasting the token into Key.)
Drag-and-drop deploys can leave the function missing (404), so use GitHub if you can.

## Test
1. Open the live page in a private window.
2. Sign up with your own email; you should see "You're in!".
3. Check the contact appears in the getfastforward list in SendFox.
4. Make sure the SendFox automation for list 618152 is on (the thank-you text promises a "you're in" email).

## Images
- `images/book-scene.webp`: the café scene from the book (cropped by the page to fit; change `object-position` on `.scene img` to move the crop)
- `images/hare.png`: the running hare from the cover
- `images/signature-white.png`: signature in the footer
- `images/logos/`: white client logos (shown on the pink background)
