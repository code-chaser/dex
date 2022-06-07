<h1 align="center"> Commands & Features </h1>

___


<table align="center">
<thead>
<tr>
  <th colspan=4 align="center"><h3>- - - - - - -  C O M M A N D S  - - - - - - -</h3></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">#</td>
<td align="left">COMMAND</td>
<td align="left">FUNCTION</td>
<td align="center">ALIASES</td>
</tr>
<tr>
<td align="center">1</td>
<td align="left"><code>$dex</code></td>
<td align="left">default set prefix</td>
<td align="left"><i><b>N/A</b></i></td>
</tr>
<tr>
<td align="center">2</td>
<td align="left"><code>&lt;prefix&gt; help</code></td>
<td align="left">shows the list of all commands</td>
<td align="left"><i><b>N/A</b></i></td>
</tr>
<tr>
<td align="center">3</td>
<td align="left"><code>&lt;prefix&gt; changepref &lt;p&gt;</code></td>
<td align="left">sets the prefix for the server as <code>&lt;p&gt;</code></td>
<td align="left"><code>changeprefix</code></td>
</tr>
<tr>
<td align="center">4</td>
<td align="left"><code>&lt;prefix&gt; tags &lt;on/off&gt;</code></td>
<td align="left">toggles message tags (on/off)</td>
  <td align="left"><code>msgtag</code>,<code>tagging</code></td>
</tr>
<tr>
<td align="center">5</td>
<td align="left"><code>&lt;prefix&gt; inspire</code></td>
<td align="left">sends a random inspirational quote</td>
<td align="left"><code>iquote</code></td>
</tr>
<tr>
<td align="center">6</td>
<td align="left"><code>&lt;prefix&gt; astropic</code></td>
<td align="left">sends NASA's astronomy pic of the day</td>
<td align="left"><code>astropicotd</code>, <code>nasapic</code>, <code>nasapicotd</code></td>
</tr>
<tr>
<td align="center">7</td>
<td align="left"><code>&lt;prefix&gt; covid19 &lt;country&gt;</code></td>
<td align="left">sends COVID-19 stats of the given country (global stats if country == <code>null</code>)</td>
<td align="left"><i><b>N/A</b></i></td>
</tr>
<tr>
<td align="center">8</td>
<td align="left"><code>&lt;prefix&gt; meme</code></td>
<td align="left">sends a random meme</td>
<td align="left"><i><b>N/A</b></i></td>
</tr>
<tr>
<td align="center">9</td>
<td align="left"><code>&lt;prefix&gt; subreddit &lt;topic&gt; &lt;number_of_headlines&gt;</code></td>
<td align="left">sends top n headlines from the given subreddit</br><code>n = min(available,requested)</code></td>
<td align="left"><code>reddit</code></td>
</tr>
<tr>
<td align="center">10</td>
<td align="left"><code>&lt;prefix&gt; userinfo &lt;uID&gt;</code></td>
<td align="left">shows user info of <code>&lt;uID&gt;</code>, if it's valid, else the message author</td>
<td align="left"><code>ui</code>, <code>memberinfo</code>, <code>mi</code></td>
</tr>
<tr>
<td align="center">11</td>
<td align="left"><code>&lt;prefix&gt; serverinfo</code></td>
<td align="left">shows server (guild) info</td>
<td align="left"><code>si</code>, <code>guildinfo</code>, <code>gi</code></td>
</tr>
<tr>
<td align="center">12</td>
<td align="left"><code>&lt;prefix&gt; join</code>, <code>&lt;prefix&gt; leave</code></td>
<td align="left">joins and leaves the voice channel respectively</td>
<td align="left"><code>connect</code>, <code>disconnect</code></td>
</tr>
<tr>
<td align="center">13</td>
<td align="left"><code>&lt;prefix&gt; play &lt;query&gt;</code></td>
<td align="left">joins the voice channel of the author and starts playing the first track (or queues it if already playing) from the search results (from YT) of the given <code>query</code></td>
<td align="left"><code>p</code>, <code>stream</code>, <code>add</code>, <code>queue</code></td>
</tr>
<tr>
<td align="center">14</td>
<td align="left"><code>&lt;prefix&gt; dplay &lt;query&gt;</code></td>
<td align="left">same as <code>play</code> except that it first <b>downloads</b> the given track then plays to reduce any possible lags<br><i>NOTE: there might still be some lag due to the latency between the bot's hosting server (EU) and the user side</i></td>
<td align="left"><i><b>N/A</b></i></td>
</tr>
<tr>
<td align="center">15</td>
<td align="left"><code>&lt;prefix&gt; pause</code><br><code>&lt;prefix&gt; resume</code></td>
<td align="left">pauses, resumes the currently playing track, respectively</td>
<td align="left">(for <b>resume</b>):- <code>play</code> <i>(without any query)</i></td>
</tr>
<tr>
<td align="center">16</td>
<td align="left"><code>&lt;prefix&gt; stop</code></td>
<td align="left">stops currently playing track and clears the queue</td>
<td align="left"><code>shut</code></td>
</tr>
<tr>
<td align="center">17</td>
  <td align="left"><code>&lt;prefix&gt; queue <b><strike>&lt;query&gt;</strike></b></code></td>
<td align="left">shows the complete queue</td>
<td align="left"><code>view</code></td>
</tr>
<tr>
<td align="center">18</td>
<td align="left">
  <ul>
    <li><code>&lt;prefix&gt; skip </code></li>
    <li><code>&lt;prefix&gt; jump &lt;#track&gt;</code></li>
    <li><code>&lt;prefix&gt; remove &lt;#track&gt;</code></li>
  </ul>
</td>
<td align="left">
  <ul>
    <li>skips the current track</li>
    <li>jumps to the given track number</li>
    <li>removes the given track number from the queue</li>
  </ul>
</td>
<td align="left">
  <ul>
    <li><code>next</code></li>
    <li><b><i>N/A</i></b></li>
    <li><b><i>N/A</i></b></li>
  </ul>
</td>
</tr>
<tr>
<td align="center">19</td>
<td align="left"><code>&lt;prefix&gt; volume &lt;vol_in_%&gt;</code></td>
<td align="left">sets the volume of the bot to given value</td>
<td align="left"><b><i>N/A</i></b></td>
</tr>
<tr>
<td align="center">20</td>
<td align="left"><code>&lt;prefix&gt; ping</code></td>
<td align="left">shows the latency of the bot</td>
<td align="left"><code>latency</code></td>
</tr>
</tbody>
</table>




<!--|S. No.|COMMAND|FUNCTION|ALIASES|
|:-:|:-:|:-|:-:|
|1|`$dex`|default set prefix|N/A|
|2|`<prefix> help`|shows the list of all commands|N/A|
|3|`<prefix> changepref <p>`|sets the prefix for the server as `<p>`|`chngpref`|
|4|`<prefix> inspire`|sends a random inspirational quote|N/A|
|5|`<prefix> userinfo`|shows user info of the message author|`ui`, `memberinfo`, `mi`|
|6|`<prefix> userinfo <uID>`|shows user info of `<uID>` if it's valid else the message author|`ui`, `memberinfo`, `mi`|
|7|`<prefix> serverinfo`|shows server (guild) info|`si`, `guildinfo`, `gi`|
```
$dex                     - default set prefix;
<prefix> help            - shows the list of all commands;
<prefix> changepref <p>  - sets the prefix for the server as <p>;
<prefix> inspire         - sends an inspirational quote;
<prefix> userinfo        - shows user info of the message author;
<prefix> userinfo <uID>  - shows user info of <uID> if it's valid else the message author;
<prefix> serverinfo      - shows server (guild) info;
```
-->


___

<!--|Check|Feature|
|:-:|:-|
| ✔️ | Server custom prefixes |
| ✔️ | Message Tags |
| ✔️ | Inspirational Quotes |
| ✔️ | Astronomy Pic OTD by NASA |
| ✔️ | COVID 19 statistics |
| ✔️ | Memes |
| ✔️ | Shows User Information |
| ✔️ | Shows Server Information |
|    | Plays Music | -->

<!--
<table align = "center">
<thead>
<tr>
  <th colspan=4 align="center"><h3>- - - - - - -  F E A T U R E S  - - - - - - -</h3></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">Check</td>
<td align="left">Feature</td>
<td align="left">API Used</td>
<td align="left">Permissions Required by the BOT</td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Server custom prefixes</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Message Tags</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Inspirational Quotes</td>
<td align="left"><a href="https://premium.zenquotes.io/zenquotes-documentation/"><b>ZenQuotes API</b></a></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Astronomy Pic of the day by NASA</td>
<td align="left"><a href="https://api.nasa.gov/"><b>NASA APOD API</b></a></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">COVID-19 Stats</td>
<td align="left"><a href="https://documenter.getpostman.com/view/10808728/SzS8rjbc"><b>Coronavirus COVID-19 API v1</b></a></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Memes</td>
<td align="left"><a href="https://github.com/D3vd/Meme_Api"><b>D3vd/Meme_Api</b></a></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">SubReddits</td>
<td align="left"><a href="https://www.reddit.com/dev/api/"><b>Reddit API</b></a></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Shows User Information</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Shows Server Information</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages, Ban Members, Manage Server</i></td>
</tr>
<tr>
<td align="center"><g-emoji class="g-emoji" alias="heavy_check_mark" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/2714.png">✔️</g-emoji></td>
<td align="left">Plays Music</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages, Connect to Voice Channels, Use Voice Activity, Speak, Unmute</i></td>
</tr>
</tbody>
</table>
-->

___
