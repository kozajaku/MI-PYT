<h1 id="betamax-testing">betamax testing</h1>
<p>To invoke new cassettes recording for betamax testing, simply setup new environment variable named <strong>AUTH_FILE</strong> pointing to path to a configuration file with valid credentials. For instance, to start testing by recording new cassettes, invoke:</p>
<div class="sourceCode"><pre class="sourceCode bash"><code class="sourceCode bash"><span class="ot">AUTH_FILE=</span>auth.cfg <span class="kw">python</span> setup.py test</code></pre></div>
<p>or</p>
<div class="sourceCode"><pre class="sourceCode bash"><code class="sourceCode bash"><span class="ot">AUTH_FILE=</span>auth.cfg <span class="kw">pytest</span> tests</code></pre></div>
<p>where <em>auth.cfg</em> is name of the configuration file.</p>
<p>In order to use already recorded cassettes simple omit the environment variable:</p>
<div class="sourceCode"><pre class="sourceCode bash"><code class="sourceCode bash"><span class="kw">python</span> setup.py test</code></pre></div>
<p>or</p>
<div class="sourceCode"><pre class="sourceCode bash"><code class="sourceCode bash"><span class="kw">pytest</span> tests</code></pre></div>
<h1 id="twitter.py-help">twitter.py help</h1>
<pre><code>Usage: twitter.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  console  Simple tool that uses Twitter API to...
  web      Web frontend for Twitter Wall tool.</code></pre>
<h1 id="twitter.py-console-help">twitter.py console help</h1>
<pre><code>Usage: twitter.py console [OPTIONS]

  Simple tool that uses Twitter API to periodically check in infinite loop
  new tweets satisfying search expression. This tool depends on a
  configuration file which must be provided by the user. The configuration
  file contains Twitter API key and secret properties, that are afterwards
  used for authentication purposes.

Options:
  --config TEXT                 Path to a configuration file with Twitter API
                                keys.
  -s, --search TEXT             Expression to be searched on Twitter.
  -c, --count INTEGER           Count of tweets to be queried during initial
                                wave.
  -i, --interval INTEGER        Interval in seconds specifying time period to
                                query new tweets.
  -v, --verbose                 Show additional output.
  --lang TEXT                   Restricts tweets to the given language, given
                                by an ISO 639-1 code.
  --retweeted / --no-retweeted  Enable or disable showing of retweets.
  --show-id                     Show tweet&#39;s ID
  --show-date                   Show tweet&#39;s creation date.
  --show-name                   Show tweet&#39;s author name.
  --show-screen-name            Show tweet&#39;s author twitter nickname.
  --help                        Show this message and exit.</code></pre>
<h1 id="twitter.py-web-help">twitter.py web help</h1>
<pre><code>Usage: twitter.py web [OPTIONS]

  Web frontend for Twitter Wall tool. User can query specified twitter
  search expression on simple web page and show results in simple format
  including all additional tweet entities.

Options:
  --debug         Setup debug flags for Flask application.
  --port INTEGER  TCP port of the web server.
  --host TEXT     The hostname to listen on.
  --config TEXT   Path to a configuration file with Twitter API keys.
  --help          Show this message and exit.</code></pre>
<h1 id="configuration-file">configuration file</h1>
<p>In order to be able to properly start twitter wall tool, it is necessary to create configuration file containing OAuth credentials to authenticate into Twitter API. The configuration file has following form:</p>
<pre><code>[twitter]
key=XXXXXXXXXX
secret=YYYYYYYYY</code></pre>
<p>Of course, <em>XXXXXXXXXX</em> and <em>YYYYYYYYY</em> must be replaced for correct Twitter API key and secret. Twitter wall tool will implicitly look for configuration file named auth.cfg in executed directory, however this behavior can be changed using <em>--config</em> parameter.</p>
