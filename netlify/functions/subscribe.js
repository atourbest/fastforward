// Adds a sign-up to a SendFox list. Used by the mini course page (/) and the free book pages (/free-book, /who-am-i-really).
// Needs the SENDFOX_API_KEY environment variable on Netlify.

// Only these lists can be signed up to from this site.
// Free book lists have a required consent box; the server checks it too.
const CONSENT_LISTS = [686129, 686440];

const ALLOWED_LISTS = [
  618152, // getfastforward (5-day mini course)
  686129, // FAST Forward free book
  686440, // Who Am I Really free book
];

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method not allowed' };
  }
  let body;
  try { body = JSON.parse(event.body); }
  catch { return { statusCode: 400, body: JSON.stringify({ error: 'Invalid JSON' }) }; }

  const { email, listId, firstName, consent } = body;
  if (!email || !listId) {
    return { statusCode: 400, body: JSON.stringify({ error: 'email and listId required' }) };
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email address' }) };
  }
  const list = parseInt(listId, 10);
  if (!ALLOWED_LISTS.includes(list)) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Unknown list' }) };
  }
  // The free book form has a required consent box; the server checks it too.
  if (CONSENT_LISTS.includes(list) && consent !== true) {
    return { statusCode: 400, body: JSON.stringify({ error: 'Please tick the box to agree to receive emails.' }) };
  }
  const apiKey = process.env.SENDFOX_API_KEY;
  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Server configuration error' }) };
  }

  const contact = { email, lists: [list] };
  if (firstName && String(firstName).trim()) contact.first_name = String(firstName).trim().slice(0, 100);

  try {
    const response = await fetch('https://api.sendfox.com/contacts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
      body: JSON.stringify(contact)
    });
    const data = await response.json();
    // 422 treated as "already exists" -- ASSUMPTION, verify against SendFox docs
    if (response.ok || response.status === 422) {
      return { statusCode: 200, headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ success: true }) };
    }
    return { statusCode: response.status, body: JSON.stringify({ error: data.message || 'Signup failed' }) };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Network error' }) };
  }
};
