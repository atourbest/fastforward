"""Builds the Who Am I Really? course pages (/wair/day-1/ ... /wair/day-5/, /wair/bonus/, /wair/skill/).

The copy-and-paste prompts are generated from the coaching skill (SKILL.md), so the prompts and
the skill always match. Re-run after changing the skill:
    python3 wair/build_pages.py path/to/who-am-i-really-coach/SKILL.md
"""
import html, os, re, sys

SKILL = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ZIP = 'who-am-i-really-coach.zip'

src = open(SKILL, encoding='utf-8').read()
body = src.split('---', 2)[2]
sections = {}
for part in re.split(r'\n(?=## )', body):
    m = re.match(r'## (.+)\n', part)
    if m:
        sections[m.group(1).strip()] = part.strip()
intro = re.search(r'^The idea behind it.*$', body, re.M).group(0).strip()  # Jason's framing of the course

def day_key(n):
    return next(k for k in sections if k.startswith(f'Day {n} '))

def build_prompt(n):
    common = [sections['How to coach'], sections['Care and privacy'], sections['The buddy'], sections['The Brand File']]
    brand = common[3].replace("Tomorrow, start a new chat with 'Start Day N' and paste it in.",
                              "Tomorrow, open the next day's prompt from Jason's email, paste it into a new chat, then paste this in.")
    common[3] = brand
    if n == 1:
        start = 'Start now: welcome me and begin Day 1 with the first step. Ask one question at a time.'
    else:
        start = (f'Start now: ask me to paste my Brand File from the day before. If I don\'t have one, offer a quick '
                 f'catch-up of two or three questions. Then begin Day {n}. Ask one question at a time.')
    return '\n\n'.join([
        f'You are my coach for Day {n} of Jason Moore\'s 5-day course "Who Am I Really? Uncover your personal brand story". '
        'Follow these instructions for the whole conversation.',
        intro, *common, sections[day_key(n)], start])

DAYS = {
    1: dict(title='You already have a brand', mins='10 to 20 minutes',
            lead=['Right now, someone is talking about you. In a calibration session. In a top-talent meeting. In a chat by the coffee machine. That’s your brand: what people say about you when you leave the room.',
                  'You can’t make it up. But you can go in search of it. Today you’ll write a quick, honest baseline, then look at the brands you love. The brands we choose say more about us than we think.'],
            buddy='Swap your three brands and talk about what surprised you.',
            next='Strengths and passions. And a twist involving your heroes.'),
    2: dict(title='Strengths and passions', mins='10 to 20 minutes',
            lead=['Think of your brand as an iceberg. Some of it is easy to see: what you do, how you behave, what you’ve achieved. Most of it sits below the surface.',
                  'Today you start at the top: your strengths and your passions. You’ll pick a hero or two, then cross out their name and put yours in. You may be surprised how many of their qualities are already yours.'],
            buddy='Share your heroes and ask if they agree the qualities fit you.',
            next='Values and personality. In three emoji.'),
    3: dict(title='Values and personality', mins='10 to 20 minutes',
            lead=['Your values formed when you were young: your family, how you were raised, the big moments in your life. You probably don’t think about them much. But they quietly drive almost every decision you make.',
                  'Today you’ll pick ten values, cut them to five, then three. It’s harder than it sounds. Then you’ll look at your personality in a way you might not expect: three emoji. Yours, and the three someone who knows you would pick.'],
            buddy='Pick three emoji for each other before you reveal your own.',
            next='The moments that made you, and your story.'),
    4: dict(title='Your story', mins='15 to 20 minutes',
            lead=['Most of life slips by unremembered. But a handful of moments define who we become. Mine started before I was born, when my grandparents adopted my orphaned, infant father.',
                  'Today you’ll find three or four of your defining moments. You choose what to share; highs alone are fine. Then you’ll turn everything from this week into your personal brand story, in three short parts: <strong>Once upon a time…</strong> <strong>Because of that…</strong> <strong>Every day…</strong> The whole thing takes less than 90 seconds to tell.'],
            buddy='Tell your story out loud and ask two questions. What worked? What could make it even better?',
            next='How to introduce yourself in under 15 seconds.'),
    5: dict(title='Introduce yourself', mins='10 to 20 minutes',
            lead=['People make judgements about us in a fraction of a second. Then they look for evidence that they were right. A clear introduction helps you shape that first impression.',
                  'Today you’ll turn your story into an introduction that takes less than 15 seconds: <strong>I</strong> (headline)… <strong>by</strong> (actions)… <strong>for example</strong>… Here’s mine: <em>I help people do their best work by creating tools, sharing stories and connecting ideas. For example, I wrote a book and designed an app that helps people uncover and share their personal brand.</em>'],
            buddy='Try your introduction on one person this week. Then hit reply to any of my emails and tell me how it went.',
            next='One more thing: a bonus chapter on your origin story.'),
}

HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light only">
<meta name="robots" content="noindex, nofollow">
<title>{title} · Who Am I Really?</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Work+Sans:wght@700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../wair.css">
</head>
<body>

<main class="page">
  <article class="card">
    <div class="inner">
'''

FOOT = '''      <div class="signoff">
        <p>Talk soon,</p>
        <img class="sig-jason" src="../../images/signature-jason.png" alt="Jason">
        <p class="byline"><strong>Jason Moore</strong><br>Author of <em>Who Am I Really?</em></p>
      </div>
    </div>

    <aside class="book" aria-labelledby="book-title">
      <div class="pic"><img src="../../images/wair-mockup.webp" alt="Who Am I Really? paperback cover"></div>
      <div class="copy">
        <h2 id="book-title">Prefer <em>pen and paper?</em></h2>
        <p>Every exercise in this course comes from my workbook, <em>Who Am I Really?</em> The paperback has space on every page to write your answers.</p>
        <a class="btn" href="https://www.amazon.com/Who-really-Uncover-Personal-Story/dp/199961805X" target="_blank" rel="noopener">Get the paperback →</a>
      </div>
    </aside>
  </article>

  <footer>
    <img class="fox" src="../../images/fox-gold.png" alt="">
    <img class="sig" src="../../images/signature-white.png" alt="Jason Moore">
    <p class="copy">© Jason Moore. All rights reserved.</p>
  </footer>
</main>
{script}
</body>
</html>
'''

COPY_JS = '''
<script>
document.querySelectorAll('[data-copy]').forEach(function(btn){
  btn.addEventListener('click', function(){
    var text = document.getElementById(btn.getAttribute('data-copy')).textContent;
    var label = btn.textContent;
    function done(){ btn.textContent = 'Copied ✓'; setTimeout(function(){ btn.textContent = label; }, 2000); }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
    function fallback(){
      var t = document.createElement('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.appendChild(t); t.select();
      try { document.execCommand('copy'); done(); } catch(e) { btn.textContent = 'Select the text and copy it'; }
      document.body.removeChild(t);
    }
  });
});
</script>'''

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l10.5-6.5z"/></svg>'

def progress(n, label):
    bars = ''.join('<li class="done"></li>' if i <= n else '<li></li>' for i in range(1, 6))
    return f'''      <div class="progress">
        <p class="kicker">{label}</p>
        <ol class="steps" aria-label="{label}">{bars}</ol>
      </div>
'''

def video(title):
    # Placeholder until the video is filmed: replace the .placeholder div with the embed iframe.
    return f'''      <div class="video" id="video">
        <div class="placeholder"><div class="play"></div><span>Video coming soon</span></div>
      </div>
      <p class="length">Under 3 minutes</p>
'''

def day_page(n, d):
    prompt = html.escape(build_prompt(n), quote=False)
    paste = '' if n == 1 else ' and paste in your Brand File'
    leads = ''.join(f'      <p class="lead">{p}</p>\n' for p in d['lead'])
    out = HEAD.format(title=f'Day {n}: {d["title"]}')
    out += progress(n, f'Who Am I Really? · Day {n} of 5')
    out += f'      <h1>{d["title"]}</h1>\n\n' + video(d['title']) + '\n' + leads
    out += f'''
      <section class="session">
        <p class="label">{PLAY}Today’s coaching session</p>
        <h2>About {d["mins"]} with your AI coach</h2>

        <div class="option">
          <h3>Using the Claude skill?</h3>
          <p>Start a new chat, type <span class="cmd">Start Day {n}</span>{paste}. That’s it.</p>
        </div>

        <div class="option">
          <h3>Using any other AI?</h3>
          <p>Copy this prompt and paste it into a new chat in Claude, ChatGPT, Gemini or Copilot.{' Then paste in your Brand File when your coach asks for it.' if n > 1 else ''}</p>
          <div class="prompt">
            <pre id="prompt">{prompt}</pre>
            <div class="bar"><span>Day {n} prompt</span><button class="btn" type="button" data-copy="prompt">Copy the prompt</button></div>
          </div>
        </div>
        <p class="note">At the end, your coach will give you your Brand File. Copy it and save it somewhere safe.{' You’ll need it tomorrow.' if n < 5 else ' It now holds your story.'}</p>
      </section>

      <section class="block">
        <p class="label plain">Buddy</p>
        <p>{d["buddy"]}</p>
      </section>

      <section class="block">
        <p class="label plain">{'Coming tomorrow' if n < 5 else 'Coming next'}</p>
        <p>{d["next"]}</p>
      </section>

'''
    out += FOOT.format(script=COPY_JS)
    return out

def bonus_page():
    out = HEAD.format(title='Your origin story')
    out += progress(5, 'Who Am I Really? · Bonus chapter')
    out += '      <h1>Your origin story</h1>\n\n' + video('Your origin story') + '\n'
    out += '''      <p class="lead">Your personal brand story says who you are. Your origin story says how you came to know what you know. It’s the story to tell when you teach, lead, pitch or present, and you want people to trust what comes next.</p>
      <p class="lead">[PLACEHOLDER: one or two sentences introducing the 8 steps.]</p>

      <section class="block">
        <p class="label plain">The bonus chapter</p>
        <p>[PLACEHOLDER: short description of what’s in the PDF.]</p>
        <p style="margin-top:14px"><span class="btn big disabled" aria-disabled="true">PDF coming soon</span></p>
      </section>

      <section class="session">
        <p class="label">''' + PLAY + '''Work on it with your coach</p>
        <h2>About 20 minutes with your AI coach</h2>
        <div class="option">
          <h3>Using the Claude skill?</h3>
          <p>Start a new chat, type <span class="cmd">Start my origin story</span> and paste in your Brand File. [PLACEHOLDER: confirm once added to the skill.]</p>
        </div>
        <div class="option">
          <h3>Using any other AI?</h3>
          <p>[PLACEHOLDER: the origin story prompt goes here, with a copy button, once the 8 steps are added.]</p>
        </div>
      </section>

      <section class="block">
        <p class="label plain">What’s next</p>
        <p>Once you know your story, find out how it lands. My free 5-day email course shows you how to get feedback you’ll love by asking for advice instead. <a href="/">Start the free course →</a></p>
      </section>

'''
    out += FOOT.format(script='')
    return out

def skill_page():
    out = HEAD.format(title='Set up your AI coach')
    out += progress(0, 'Who Am I Really? · Set-up')
    out += '''      <h1>Set up your AI coach</h1>
      <p class="lead">Your coach knows the whole course. It asks one question at a time, notices patterns in your answers, and helps you draft your story in your own words. Pick the option that suits you.</p>

      <section class="session">
        <p class="label">''' + PLAY + '''Option A: the coaching skill for Claude</p>
        <h2>About 5 minutes to set up</h2>
        <p style="margin-top:16px"><a class="btn big" href="../downloads/''' + SKILL_ZIP + '''" download>Download the coach</a></p>
        <div class="option">
          <h3>Then, in Claude:</h3>
          <ol style="margin:8px 0 0 22px;display:grid;gap:6px;font-size:16.5px;line-height:1.5">
            <li>Go to <strong>Settings › Capabilities</strong> and turn on <strong>code execution</strong>.</li>
            <li>Go to <strong>Customize › Skills</strong>, click <strong>+</strong>, then <strong>Create skill › Upload a skill</strong>.</li>
            <li>Upload the file you downloaded (don’t unzip it) and switch the skill on.</li>
            <li>Start a new chat and type <span class="cmd">Start Day 1</span></li>
          </ol>
        </div>
        <div class="option">
          <h3>Using ChatGPT?</h3>
          <p>[PLACEHOLDER: ChatGPT steps, once tested.]</p>
        </div>
      </section>

      <section class="block">
        <p class="label plain">Option B: no set-up</p>
        <p>Each day’s email links to a page with a prompt. Copy it, paste it into the AI tool you already use (Claude, ChatGPT, Gemini or Copilot), and the coaching starts. <a href="../day-1/">See the Day 1 page →</a></p>
      </section>

      <section class="block">
        <p class="label plain">Your Brand File</p>
        <p>At the end of each day, your coach writes a short summary of your answers. That’s your Brand File. Save it somewhere safe: a note on your phone, a document, an email to yourself. The next day, paste it in and your coach picks up where you left off.</p>
      </section>

      <section class="block">
        <p class="label plain">A note on privacy</p>
        <p>You’ll be talking about your values, your strengths and some of the moments that shaped you. Share only what you’re comfortable with. If you use AI at work, think about using a personal account for this instead.</p>
      </section>

'''
    out += FOOT.format(script='')
    return out

pages = {f'day-{n}': day_page(n, d) for n, d in DAYS.items()}
pages['bonus'] = bonus_page()
pages['skill'] = skill_page()
for slug, page in pages.items():
    os.makedirs(os.path.join(HERE, slug), exist_ok=True)
    open(os.path.join(HERE, slug, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', slug)
