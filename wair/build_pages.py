"""Builds the Who Am I Really? course pages (/wair/day-1/ ... /wair/day-5/, /wair/bonus/, /wair/skill/).

The coach lives in one AI project (a Claude Project, ChatGPT project or Gemini Gem) that holds the project
instructions and the coaching file. The copy-and-paste prompts on the day pages are generated from that same
coaching file, so the prompts and the project coach always match. Re-run after changing the coaching file:
    python3 wair/build_pages.py            (defaults to wair/downloads/who-am-i-really-coach.md)
    python3 wair/build_pages.py path/to/who-am-i-really-coach.md

/wair/skill/ keeps its old address (emails link to it) but is now the project set-up page.
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
COACH_FILE = 'who-am-i-really-coach.md'
INSTRUCTIONS_FILE = 'project-instructions.txt'
SOURCE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'downloads', COACH_FILE)

# PLACEHOLDER: replace with the Career in Motion purchase page URL when it exists.
CIM_URL = '#career-in-motion'

src = open(SOURCE, encoding='utf-8').read()
# The coaching file is: copyright notice, ---, instructions, ---, closing copyright line.
parts = src.split('\n---\n')
notice, body = parts[0], '\n---\n'.join(parts[1:-1])
sections = {}
for part in re.split(r'\n(?=## )', body):
    m = re.match(r'## (.+)\n', part)
    if m:
        sections[m.group(1).strip()] = part.strip()
intro = re.search(r'^The idea behind it.*$', body, re.M).group(0).strip()  # Jason's framing of the course
instructions = open(os.path.join(HERE, 'downloads', INSTRUCTIONS_FILE), encoding='utf-8').read().strip()

PROMPT_COPYRIGHT = ('© 2020–2026 Jason Moore. All rights reserved. This prompt is licensed for your personal use only. '
                    'Please don\'t copy, share or adapt it.')

def day_key(n):
    return next(k for k in sections if k.startswith(f'Day {n} '))

SAVING = (
    "## Saving progress\n\n"
    "Each chat is separate, so my answers need to carry over. Whenever a day says \"Save progress\" (or if I stop early), "
    "write my updated Brand File, using the template below, in a single code block so it's easy to copy. Then tell me: "
    "\"Save this somewhere safe. Next time, open the next prompt from Jason's email, paste it into a new chat, then paste this in.\" "
    "On Day 5, also give me my finished story and introduction to keep.")

def common():
    # A pasted prompt can't rely on memory or on a project, so prompts always use the Brand File.
    return [sections['How to coach'], sections['Care and privacy'], sections['Protecting the method'],
            sections['The buddy'], SAVING, sections['The Brand File']]

def build_prompt(n):
    if n == 1:
        start = 'Start now: welcome me and begin Day 1 with the first step. Ask one question at a time.'
    else:
        start = (f'Start now: ask me to paste my Brand File from the day before. If I don\'t have one, offer a quick '
                 f'catch-up of two or three questions. Then begin Day {n}. Ask one question at a time.')
    return '\n\n'.join([
        f'You are my coach for Day {n} of Jason Moore\'s 5-day course "Who Am I Really? Uncover your personal brand story". '
        'Follow these instructions for the whole conversation.',
        intro, *common(), sections[day_key(n)], start, PROMPT_COPYRIGHT])

def build_bonus_prompt():
    start = ('Start now: ask if I have a Brand File from the 5-day course and, if so, to paste it in (it\'s optional). '
             'Then begin with the first step: finding the limiting belief. Ask one question at a time.')
    return '\n\n'.join([
        'You are my coach for the bonus chapter of Jason Moore\'s course "Who Am I Really?": my origin story. '
        'Follow these instructions for the whole conversation.',
        intro, *common(), sections['Bonus: your origin story'], start, PROMPT_COPYRIGHT])

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
            next='One more thing: a bonus chapter on your origin story. And when you’re ready, Career in Motion (below).'),
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


def project_option(cmd, first=False):
    remember = ('Your coach saves your answers as you go, so you can pick up in any new chat in the project.' if first
                else 'Your coach picks up where you left off.')
    return f'''        <div class="option">
          <h3>In your Who Am I Really? project</h3>
          <p>Open a new chat inside your project and type <span class="cmd">{cmd}</span>. {remember} Not set up yet? <a href="../skill/">Set up your project (about 3 minutes) →</a></p>
        </div>
'''

def cim_cta(heading='You know who you are. <em>Now what?</em>'):
    # PLACEHOLDER link: set CIM_URL at the top of this file to the Career in Motion purchase page.
    return f'''      <!-- PLACEHOLDER: Career in Motion purchase page link is CIM_URL in build_pages.py -->
      <section class="cim" id="career-in-motion">
        <p class="label">What’s next: Career in Motion</p>
        <h2>{heading}</h2>
        <p><em>Career in Motion</em> is my 5-day companion course. It takes everything you’ve uncovered here, your strengths, values and story, and turns it into a career plan.</p>
        <ul>
          <li>See where your time really goes, and whether it matches your story</li>
          <li>Hear what people are already telling you</li>
          <li>Choose a direction and the skills you’ll need next</li>
          <li>Find the projects and people that build the path</li>
          <li>Leave with a one-page plan and your next career conversation, practised</li>
        </ul>
        <p>It adds one file to the project you already have. Same coach, same Brand File, nothing new to learn.</p>
        <a class="btn big" href="{CIM_URL}">Get Career in Motion →</a>
      </section>

'''

def day_page(n, d):
    prompt = html.escape(build_prompt(n), quote=False)
    leads = ''.join(f'      <p class="lead">{p}</p>\n' for p in d['lead'])
    out = HEAD.format(title=f'Day {n}: {d["title"]}')
    out += progress(n, f'Who Am I Really? · Day {n} of 5')
    out += f'      <h1>{d["title"]}</h1>\n\n' + video(d['title']) + '\n' + leads
    out += f'''
      <section class="session">
        <p class="label">{PLAY}Today’s coaching session</p>
        <h2>About {d["mins"]} with your AI coach</h2>

{project_option(f"Start Day {n}", first=(n == 1))}
        <div class="option">
          <h3>No project? Use today’s prompt</h3>
          <p>Copy this prompt and paste it into a new chat in Claude, ChatGPT, Gemini or Copilot.{' Then paste in your Brand File when your coach asks for it.' if n > 1 else ''}</p>
          <div class="prompt">
            <pre id="prompt">{prompt}</pre>
            <div class="bar"><span>Day {n} prompt</span><button class="btn" type="button" data-copy="prompt">Copy the prompt</button></div>
          </div>
        </div>
        <p class="note">{'Using the prompt? At the end, your coach gives you a Brand File: a short summary of your answers. Copy it and save it somewhere safe. You’ll paste it in tomorrow.' if n < 5 else 'At the end, your coach gives you your finished story and introduction. Copy them and keep them somewhere safe.'}</p>
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
    if n == 5:
        out += cim_cta()
    out += FOOT.format(script=COPY_JS)
    return out

def bonus_page():
    prompt = html.escape(build_bonus_prompt(), quote=False)
    out = HEAD.format(title='Your origin story')
    out += progress(5, 'Who Am I Really? · Bonus chapter')
    out += '      <h1>Your origin story</h1>\n\n' + video('Your origin story') + '\n'
    out += '''      <p class="lead">Your personal brand story says who you are. Your origin story says how you came to know what you know. It’s the story to tell when you teach, lead, pitch or present, and you want people to trust what comes next.</p>
      <p class="lead">It starts with one rule: begin with a limiting belief you once held and changed, that other people still hold. Then you shape it in eight steps: <strong>Set-up</strong>, <strong>Big want</strong>, <strong>The wall</strong>, <strong>Aha moment</strong>, <strong>Steps</strong>, <strong>Reality</strong>, <strong>Result</strong> and <strong>Transformation</strong>. Told out loud, it takes under three minutes.</p>

      <section class="block">
        <p class="label plain">The bonus chapter</p>
        <p>The chapter walks through all eight steps, with my own origin story as the example.</p>
        <p style="margin-top:14px"><span class="btn big disabled" aria-disabled="true">PDF coming soon</span></p>
      </section>

      <section class="session">
        <p class="label">''' + PLAY + '''Work on it with your coach</p>
        <h2>About 20 minutes with your AI coach</h2>
''' + project_option('Start my origin story') + f'''        <div class="option">
          <h3>No project? Use this prompt</h3>
          <p>Copy this prompt and paste it into a new chat in Claude, ChatGPT, Gemini or Copilot. If you have your Brand File from the course, paste that in too.</p>
          <div class="prompt">
            <pre id="prompt">{prompt}</pre>
            <div class="bar"><span>Origin story prompt</span><button class="btn" type="button" data-copy="prompt">Copy the prompt</button></div>
          </div>
        </div>
        <p class="note">At the end, your coach gives you your finished origin story. Copy it and keep it somewhere safe.</p>
      </section>

      <section class="block">
        <p class="label plain">Find out how it lands</p>
        <p>My free 5-day email course shows you how to get feedback you’ll love by asking for advice instead. <a href="/">Start the free course →</a></p>
      </section>

'''
    out += cim_cta('Turn your story into <em>a career plan</em>')
    out += FOOT.format(script=COPY_JS)
    return out

def setup_page():
    instr = html.escape(instructions, quote=False)
    out = HEAD.format(title='Set up your AI coach')
    out += progress(0, 'Who Am I Really? · Set-up')
    out += f'''      <h1>Set up your AI coach</h1>
      <p class="lead">Your coach lives in one project in the AI assistant you already use. Set it up once, in about three minutes. After that, every new chat in the project is your coach, and it knows the whole course.</p>
      <p class="lead">It asks one question at a time, notices patterns in your answers, and helps you draft your story in your own words.</p>

      <section class="session">
        <p class="label">{PLAY}Step 1: get your two pieces</p>
        <h2>The coaching file and the project instructions</h2>
        <div class="option">
          <h3>The coaching file</h3>
          <p>This is everything your coach needs to know about the course.</p>
          <p style="margin-top:12px"><a class="btn big" href="../downloads/{COACH_FILE}" download>Download the coaching file</a></p>
        </div>
        <div class="option">
          <h3>The project instructions</h3>
          <p>You’ll paste this short text into your project in Step 2.</p>
          <div class="prompt">
            <pre id="instructions">{instr}</pre>
            <div class="bar"><span>Project instructions</span><button class="btn" type="button" data-copy="instructions">Copy the instructions</button></div>
          </div>
        </div>
        <p class="note">The coaching file is © Jason Moore and licensed for your personal use. Please don’t share or copy it.</p>
      </section>

      <section class="session">
        <p class="label">{PLAY}Step 2: create your project</p>
        <h2>Pick the AI you already use</h2>
        <p class="note">Menu and button names change from time to time, so yours may look slightly different.</p>
        <div class="option">
          <h3>Claude (recommended)</h3>
          <ol class="steps-list">
            <li>Open <strong>Projects</strong> and create a new project called <strong>Who Am I Really?</strong></li>
            <li>Open the project’s <strong>instructions</strong> and paste in the project instructions.</li>
            <li>Add the coaching file to the project’s <strong>files</strong>.</li>
            <li>Start a new chat inside the project and type <span class="cmd">Start Day 1</span></li>
          </ol>
        </div>
        <div class="option">
          <h3>ChatGPT</h3>
          <ol class="steps-list">
            <li>Create a new <strong>project</strong> (or a custom GPT, if your plan allows it) called <strong>Who Am I Really?</strong></li>
            <li>Paste the project instructions into the project’s <strong>instructions</strong>.</li>
            <li>Add the coaching file to the project’s <strong>files</strong>.</li>
            <li>Start a new chat in the project and type <span class="cmd">Start Day 1</span></li>
          </ol>
        </div>
        <div class="option">
          <h3>Gemini</h3>
          <ol class="steps-list">
            <li>Create a new <strong>Gem</strong> called <strong>Who Am I Really?</strong></li>
            <li>Paste the project instructions into the Gem’s <strong>instructions</strong>.</li>
            <li>Add the coaching file to the Gem’s <strong>knowledge</strong>.</li>
            <li>Start a chat with the Gem and type <span class="cmd">Start Day 1</span></li>
          </ol>
        </div>
      </section>

      <section class="block">
        <p class="label plain">Using your coach</p>
        <p>Open a new chat in your project for each session, then type:</p>
        <ul class="commands">
          <li><span class="cmd">Start Day 1</span> to <span class="cmd">Start Day 5</span> to work through the course, one day at a time</li>
          <li><span class="cmd">Start my origin story</span> for the bonus chapter</li>
          <li>Or just ask for help with your story in your own words</li>
        </ul>
      </section>

      <section class="block">
        <p class="label plain">How your coach remembers</p>
        <p>If your AI has memory turned on, your coach saves a short summary of your answers at the end of each day, and picks up where you left off in the next chat. You can ask it to forget at any time.</p>
        <p>If memory is off (some work accounts do this), your coach gives you a Brand File instead: a short summary of your answers. Save it somewhere safe and paste it in next time.</p>
        <p>On Day 5, either way, you get your finished story and introduction to keep.</p>
      </section>

      <section class="block">
        <p class="label plain">Rather not set anything up?</p>
        <p>Each day’s email links to a page with a prompt. Copy it, paste it into the AI tool you already use, and the coaching starts. <a href="../day-1/">See the Day 1 page →</a></p>
      </section>

      <section class="block">
        <p class="label plain">A note on privacy</p>
        <p>You’ll be talking about your values, your strengths and some of the moments that shaped you. Share only what you’re comfortable with. If you use AI at work, think about using a personal account for this instead.</p>
      </section>

'''
    out += cim_cta('Add <em>Career in Motion</em> to the same project')
    out += FOOT.format(script=COPY_JS)
    return out

pages = {f'day-{n}': day_page(n, d) for n, d in DAYS.items()}
pages['bonus'] = bonus_page()
pages['skill'] = setup_page()
for slug, page in pages.items():
    os.makedirs(os.path.join(HERE, slug), exist_ok=True)
    open(os.path.join(HERE, slug, 'index.html'), 'w', encoding='utf-8').write(page)
    print('wrote', slug)
