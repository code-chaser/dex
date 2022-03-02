<h3 align="center"><a href="https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=397590396532&scope=bot"><img src="https://user-images.githubusercontent.com/63065397/155839904-29ff9faa-f349-4d40-b21c-8f48b856e3a9.jpg" width="500"></a></h3>

<h1 align="center"> 
  
  <br>
  
  <a href="https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=397590396532&scope=bot"><i>dex</i></a> <small>discord bot</small>
  
  <br>
  
  [![Invite: Bot](https://img.shields.io/static/v1?label=%20Invite&message=dex&color=5865F2&style=for-the-badge&logo=discord)](https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=397590396532&scope=bot)
  
  [![License: MIT](https://img.shields.io/static/v1?label=License&message=MIT&color=red&style=for-the-badge&logo=giphy)](https://github.com/code-chaser/dex/blob/main/LICENSE) [![Made in: Python](https://img.shields.io/static/v1?label=Made%20in&message=Python&color=yellow&style=for-the-badge&logo=hyper)](https://github.com/code-chaser/dex/) [![Fork: Count](https://img.shields.io/github/forks/code-chaser/dex?color=blue&label=Forks&style=for-the-badge&logo=gitextensions)](https://github.com/code-chaser/dex/network/members) [![Star: Count](https://img.shields.io/github/stars/code-chaser/dex?color=brightgreen&label=Stars&style=for-the-badge&logo=icinga)](https://github.com/code-chaser/dex/stargazers) [![Follower: Count](https://img.shields.io/github/followers/code-chaser?color=cb5786&label=Followers&style=for-the-badge&logo=github)](https://github.com/code-chaser/)
  
</h1>


<h2 align="center"> DESCRIPTION </h2>
It's DEX, a multi-purpose discord bot that can be used to get user information, server (guild) information, get a random inspirational quote, random meme, covid-19 stats and much more, with options to set a custom prefix for each server.

<br>
<br>
  
- Try it on your own server: [Invite Bot](https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=397590396532&scope=bot)
- Try it in our public Bot server: [Join Here](https://discord.gg/FUqqEyBBA3)

___

<h2 align="center"> COMMANDS </h2>

<table align="center">
<thead>
<tr>
<th align="center">S. No.</th>
<th align="left">COMMAND</th>
<th align="left">FUNCTION</th>
<th align="center">ALIASES</th>
</tr>
</thead>
<tbody>
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
<td align="left"><code>&lt;prefix&gt; userinfo</code></td>
<td align="left">shows user info of the message author</td>
<td align="left"><code>ui</code>, <code>memberinfo</code>, <code>mi</code></td>
</tr>
<tr>
<td align="center">11</td>
<td align="left"><code>&lt;prefix&gt; userinfo &lt;uID&gt;</code></td>
<td align="left">shows user info of <code>&lt;uID&gt;</code>, if it's valid, else the message author</td>
<td align="left"><code>ui</code>, <code>memberinfo</code>, <code>mi</code></td>
</tr>
<tr>
<td align="center">12</td>
<td align="left"><code>&lt;prefix&gt; serverinfo</code></td>
<td align="left">shows server (guild) info</td>
<td align="left"><code>si</code>, <code>guildinfo</code>, <code>gi</code></td>
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

<h2 align="center"> FEATURES </h2>
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


<table align = "center">
<thead>
<tr>
<th align="center">Check</th>
<th align="left">Feature</th>
<th align="left">API Used</th>
<th align="left">Permissions Required by the BOT</th>
</tr>
</thead>
<tbody>
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
<td align="center"></td>
<td align="left">Plays Music</td>
<td align="left"><i><b>N/A</b></i></td>
<td align="left"><i><a href="">Basic Permissions</a>, Embed Messages, Connect to Voice Channels, Use Voice Activity, Speak, Unmute</i></td>
</tr>
</tbody>
</table>

___

<br>


___
> ***Beep boop. Boop beep!***

> ***Hope you, like it! 😛***
___
