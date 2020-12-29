__POD Website__
===============

By: _Jstith_

## Easy viewing, Easier maintenance

The idea is simple: Forget scrolling through 100 emails a day to find the pod from the night before, and simply pull up a bookmarked website instead. The POD website contains:

- The current POD (current date or the next day's after 2000) on the home page as soon as the website is opened
- A database with the pods from previous days (in case you need to find a link or a message from an old one)
- A simple search bar to find old PODs
- A feedback page for the website

How are the PODs displayed?

- PODs are rendered in Markdown, a rich text language that matches the bold and underlined text from the word document.
- Markdown and the webpage's css scripts are responsively designed, making viewing on computers, phones, and tablets clean and professional.

## How does it work?

The POD website was created using python's Flask library, and is hosted on a linux server using nginx and gunicorn to handle http and https traffic. Updating the website with new PODs is easy: Simply upload the `.docx` file to the `data/docx` folder, and the website does the rest. Files are stored as they are used, removing the need to re-render the same POD in markdown multiple times, making the site quick and lightweight.

![Update flowchart](static/img/POD%20Website%20Basic%20Update%20Functionality.png)

## Can anyone see this website?

It depends. The linux server has a firewall that can be configured to only allow traffic from the .edu subdomain. This means that vpn access for remote work will still allow people to access the website, anyone not on the .edu network (protected with a certificate) will be unable to access the website. However, pending the approval of the ditial collaboration security memo, there will be no need to keep the website private, and it can be totally forward facing, which is beneficial for accessability, particularly from phones.

## Is uptime an issue?

The linux server is hosted on `DigitalOcean`, a top rated hosting platform. As such, the website's uptime should be almost constant, and interruptions to the .edu network will not compromise the website itself, although the removal of access points to the whitelisted ips would restrict access. This is a necessary tradeoff to protect the PII on the website, but this can change pending the digital collaboration security memo mentioned above.

# Development Stuff

## Dependencies

- Python3
  - flask
    - flaskext.markdown
  - datetime
  - regex
  - subprocess
  - markdown
  - os
- Pandoc
- Shell --> is that even a dependency? Whatever it doesn't run on windows right now

I think that's everything. If you want to get a better list then run it in a blank venv and install until it runs then `pip freeze`. In the future, may implement _google drive_ api to grab the docx files straight from our google drive folder. That's what's in the `requirements.txt`, although idk why some of those are there, but it should work regardless.
## Use

I can happily say that right now the basic functions all seem to be working. Runs straight off flask with the correct dependencies installed, currently on a DigitalOcean server with `nginx` and `gunicorn`.

## Future goals

- Automate adding new documents - first part of the flowchart --> some non-website related reasons I haven't done this.
- Send feedback over ezgmail or something to get it to an email --> Don't want to get spammed though, form only has basic input validation that can be bypassed by somebody who knows what they're doing
- Remove old md documents and maybe docx after a month to reduce size on server, but not a huge issue because the size of those files is tiny. The site was created with this goal in mind. Can also be done manually, see the first bullet.
