# DCW
DesktopCryptoWatcher - Basic desktop GUI to pull and store data from public API(s) and create and evaluate ping-pong trading bots.

Status: Temporarily halted in favour of gaining some experience with bots/automation on my RHBot project, and also in the meantime leaving the logger to run to collect some more data.

Note: This is a simple application for my own personal use, and I'm using this mostly as a learning opporunity. I wanted to create my own application from scratch instead of using existing wrappers or software. I'll probably keep this ticking over in the background with small feature additions once the basic functionality has been implemented, but this isn't really intended for use by anyone else right now (although this may change).

## Implemented features:
1) Home screen containing information from the past day for top 20 currencies.
2) Detailed currency analysis page showing percentage change over multiple time periods, multiple RSI indicators for top 20 currencies.
3) Detailed chart window that shows a live chart of currency price with updates every 1 second.
4) Logging prices of top 20 currencies to csv file for bot training (built into the GUI).
5) Logging prices of top 20 currencies to csv file for bot training (lightweight standalone).


## Remaining Planned Core Features:
This list gets updated frequently as some features are moved up or down the priority queue based on personal preference, in particular if there is a bigger learning opportunity as that is the main focus of this project.
1) Bot Sandbox - read (local) historical price data, facilitate (and keep log of) buy and sell points, create performance review framework.
2) Bot Generator - generate large number of bots, based on a spectrum of input values for multiple indicators, for large scale devlopment and improvement.
3) Bot Evaluator - addition to sandbox to visualise bot performance over a spectra of markers, compare with other strategies (e.g. hodl), etc.


## Remaining Planned Additional Features
This list gets updated frequently as some features are moved up or down the priority queue based on personal preference, in particular if there is a bigger learning opportunity as that is the main focus of this project.
1) Bitfinex API Integration.
2) Functional Alerts Window.
3) More Advanced Chart/Analysis Window.
4) Functional Settings Window.
5) Wallet Window (for logging of PnL, history, etc.).


## Notes
1) The above planned core and additional features will be added as issues to track their progress. If certain features are taking a long time to develop then additional issues will be added to break down the feature into sub-parts.
2) There will be a heavy emphasis on multi-threading of tasks as that was one of the topics I identified as needing to learn more about in python, both synchronous and asynchronous.
3) The endpoint of this project will be when I'm mostly rehashing existing knowledge.
