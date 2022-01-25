# Twitter Analytic Program

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Get insights from Publicly-accessible Social Media Data within TAPs.

## Introduction 

* Twitter Analytic Program (TAP) is a dashboard made for monitoring Twitter perception. 
* Built with Python, Pandas, React, scikit-learn, Dash web framework, and Bootstrap
* Winner of Best in Fair at the 2020 Thomas A. Edison Regional Inventor Fair

![IF Screenshot 1.3.4](https://raw.githubusercontent.com/robertchenbao/Pictures/master/uPic/IF%20Screenshot%201.3.4.png)

## Problem

In the modern age, emerging companies rely on public opinion to make better business decisions. One important method to determine the public perception of a company is through social media. 

As one of the top social media platforms, Twitter provides an excellent channel for companies to gain insight. However, because Twitter generates a vast amount of data every day, it is challenging to analyze this data manually. 

## Related Work

Currently, many companies use surveys to measure public perception. For example, if an airline wants to know the experiences of customers, they may give surveys to people on randomly-selected flights. In some cases, some companies also use online surveys for a larger sample size.

However, the survey method has significant disadvantages. First, surveys are affected by under-coverage bias. People with extremely positive or negative sentiment are only a minority of the population, yet they are much more likely to express their opinions in a survey. Therefore, the majority is often underrepresented. Second, large-scale surveys usually take a long time to conduct, which means they can not reflect the perception after a big event fast enough.

## Architecture/Tech Stack

- Built with Python, Dash framework, and scikit-learn. 

![IF V2019.6](https://raw.githubusercontent.com/robertchenbao/Pictures/master/uPic/IF%20V2019.6.png)

## Advantages of TAP

TAP provides comprehensive  analysis of public opinion by avoiding the under-coverage bias. On Twitter, some people tweet directly to companies to express their opinions, yet many more people discuss the company with their friends and followers. This app can collect and analyze the perception of both groups so that every user is adequately represented. 


Twitter is an active platform, and it is easy to obtain a large sample. TAP can collect tens of thousands of tweets in a week. With a larger sample size, this app can provide a more reliable analysis of public perception. 

## “Who is this app made for?”

Marketing teams from a wide variety of companies can benefit from using TAP.

In the past, marketing teams often needed to write complex computer programs to mine social media data on a large scale. However, most teams do not have the specialized programming skills needed. 

TAP has a simple and intuitive interface for a robust analytics program. With TAP, marketing teams can research Twitter perception without any coding skills. Moreover, the app visualizes data on a dashboard, which makes monitoring Twitter perception much easier.

## Installation

1. First, pull the Github repo
2. Then, install the dependencies, and start the app!

```console
$ pip install -r requirements.txt
---> 100%

$ python src/app.py  # Start loading!
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8050/ (Press CTRL+C to quit)
```

## License 

MIT License
