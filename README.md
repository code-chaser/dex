
<h3 align="center"><a href="https://discord.com/users/946829157445296188"><img src="https://user-images.githubusercontent.com/63065397/155839904-29ff9faa-f349-4d40-b21c-8f48b856e3a9.jpg" width="500"></a></h3>


<h1 align="center"> 
  
  <br>
  
  <a href="https://discord.com/users/946829157445296188"><i>dex</i></a> <small>discord bot</small>
  
  <br>
  
  [![Invite: Dex](https://img.shields.io/static/v1?label=%20Invite&message=dex&color=5865F2&style=for-the-badge&logo=discord)](https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=335514139764&scope=bot) 🌟 [![Join: Server](https://img.shields.io/static/v1?label=%20Join&message=here&color=5865F2&style=for-the-badge&logo=discord)](https://discord.gg/ckaD5uKaqk)
  
  [![License: MIT](https://img.shields.io/static/v1?label=License&message=MIT&color=red&style=for-the-badge&logo=giphy)](https://github.com/code-chaser/dex/blob/main/LICENSE) [![Made in: Python](https://img.shields.io/static/v1?label=Made%20in&message=Python&color=yellow&style=for-the-badge&logo=python&logoColor=yellow)](https://github.com/code-chaser/dex/) [![Fork: Count](https://img.shields.io/github/forks/code-chaser/dex?color=blue&label=Forks&style=for-the-badge&logo=gitextensions)](https://github.com/code-chaser/dex/network/members) [![Star: Count](https://img.shields.io/github/stars/code-chaser/dex?color=brightgreen&label=Stars&style=for-the-badge&logo=icinga)](https://github.com/code-chaser/dex/stargazers) [![Follower: Count](https://img.shields.io/github/followers/code-chaser?color=cb5786&label=Followers&style=for-the-badge&logo=github)](https://github.com/code-chaser/)
  
</h1>

</br>

<h2 align="center"> DESCRIPTION </h2>
It's DEX, a multi-purpose discord bot that can be used to play music, get user information, server (guild) information, get a random inspirational quote, random meme, covid-19 stats and much more, with options to set a custom prefix for each server.
- Want to contribute? Please see [this](https://github.com/code-chaser/dex/blob/main/CONTRIBUTING.md).
___

Default set prefix is `$dex ` &nbsp; (yes, mind that trailing space)

- Try it in our public Bot server: [Join Here](https://discord.gg/ckaD5uKaqk)
- Try it on your own server: [Invite Bot](https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=335514139764&scope=bot)

Once the bot joins your server, you can get started with `$dex help` or `$dex user-manual` to get the complete list of available commands.
___

</br>

<h2 align="center"> DEMO VIDEO </h2>


https://user-images.githubusercontent.com/63065397/176365615-b1a43fd8-ea54-40ac-a247-132b6b0efd65.mp4


___

</br>

<h2 align="center"> DEPENDENCIES </h2>
<p align="center"><b>PYTHON == <code>3.9.10</code></b>

<table align="center">


<tr>

<th>Module</th>
<th>Version</th>
<th>Installation</th>
<th>Description</th>

</tr>


<tr>
<td><b>discord.py</b></td>
<td><code>1.7.3</code></td>
<td>

```bash
pip install discord.py==1.7.3
```

</td>
<td>

- Well, this is the backbone of the bot!

</td>
</tr>


<tr>
<td><b>youtube_dl</b></td>
<td><code>2021.12.17</code></td>
<td>

```bash
pip install youtube_dl==2021.12.17
```

</td>
<td>

- Fetches music data from YouTube;
- Commands `play`, `playm`, `dplay`, `dplaym` depend on this;

</td>
</tr>


<tr>
<td><b>aiohttp</b></td>
<td><code>3.7.4</code></td>
<td>

```bash
pip install aiohttp==3.7.4
```

</td>
<td>

- Library for making async HTTP requests;
- Commands `inspire`, `apod`, `meme`, `reddit`, `covid-19`, `lyrics`, `cf-handle` depend on this;

</td>
</tr>


<tr>
<td><b>async-timeout</b></td>
<td><code>3.0.1</code></td>
<td>

```bash
pip install async-timeout==3.0.1
```

</td>
<td>

- Asyncio compatible timeout context manager;

</td>
</tr>


<tr>
<td><b>typing</b></td>
<td><code>3.7.4.3</code></td>
<td>

```bash
pip install typing==3.7.4.3
```

</td>
<td>

- Required for type hinting in python;
- Installation not required for python`>=3.5`;

</td>
</tr>


<tr>
<td><b>asyncio</b></td>
<td><code>3.4.3</code></td>
<td>

```bash
pip install asyncio==3.4.3
```

</td>
<td>

- Required for writing concurrent code in python;
- Installation not required for python`>=3.4`;

</td>
</tr>


<tr>
<td><b>asyncpg</b></td>
<td><code>0.25.0</code></td>
<td>

```bash
pip install asyncpg==0.25.0
```

</td>
<td>

- Library for making async postgreSQL queries;
- Required for all the database queries;
- Server custom prefix is fetched using this library;

</td>
</tr>
</table>

<!--

- **discord.py**:
  - version = `1.7.3`
  - installation:
    ```bash
    pip install discord.py==1.7.3
    ```
  - import:
    ```python
    import discord
    ```
- **youtube_dl**:
  - version = `2021.12.17`
  - installation:
    ```bash
    pip install youtube_dl==2021.12.17
    ```
  - import:
    ```python
    import youtube_dl
    ```
- **aiohttp**:
  - version = `3.7.4`
  - installation:
    ```bash
    pip install aiohttp==3.7.4
    ```
  - import:
    ```python
    import aiohttp
    ```
- **async-timeout**:
  - version = `3.0.1`
  - installation:
    ```bash
    pip install async-timeout==3.0.1
    ```
  - import:
    ```python
    import async-timeout
    ```
- **typing**:
  - version = `3.7.4.3`
  - installation:
    ```bash
    pip install typing==3.7.4.3
    ```
  - import:
    ```python
    import typing
    ```
- **asyncio**:
  - version = `3.4.3`
  - installation:
    ```bash
    pip install asyncio==3.4.3
    ```
  - import:
    ```python
    import asyncio
    ```
- **asyncpg**:
  - version = `0.25.0`
  - installation:
    ```bash
    pip install asyncpg==0.25.0
    ```
  - import:
    ```python
    import asyncpg
    ```
-->    

___

</br>

<h2 align="center">Self Hosting Dex</h2>

I would rather advise you to not run a direct cloned instance of Dex. It would be a lot better if you just [invite](https://discord.com/api/oauth2/authorize?client_id=946829157445296188&permissions=335514139764&scope=bot) it to your discord server for testing purposes. The source code is made publicly available for educational purposes and for transparency on how Dex works.

If you decide to edit, compile or use this code in any way, kindly abide by the [License](./LICENSE).

</br>

___


<p align="center"><a href="https://github.com/code-chaser/dex#"><img src="http://randojs.com/images/backToTopButtonTransparentBackground.png" alt="Back to top" height="29"/></a></p>

___

### Please see:
- License: [code-chaser/dex/LICENSE](./LICENSE)
- Code of Conduct: [code-chaser/dex/CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
___

</br>


___
  
> ***Beep boop. Boop beep! 🤖*** ***Hope you like it! 😛***

> ***Thanks for the visit!***
___
