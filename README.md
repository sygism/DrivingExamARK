# DrivingExamARK

DrivingExamARK program was designed for the purpose of finding an open driving exam time on the Estonian DMV website, when the median waiting time was ~3 months
(ca 2020). The program allows the user to select a city and then periodically check whether an exam time has opened up in said city in the current and the next month.
When a suitable exam time has been found, a notification will be sent to the user's entered email.

## Getting Started

Python3, aswell as the required packages, are needed to execute the program.

To run the program from **bash**/**cmd** etc,

<code>python3 main.py</code>

### Prerequisites

Requirements for the software and other tools to build, test and push 
- <a href="https://pypi.org/project/requests/">requests</a>
- <a href="https://pypi.org/project/beautifulsoup4">beautifulsoup4</a>
- <a href="">smtplib</a>
- <a href="">tkinter</a>
- <a href="">datetime</a>
- <a href="">threading</a>

An email account with application passwords is required for the usage of this program. A nice tutorial about it can be found [here](https://www.interviewqs.com/blog/py-email).

## Authors

  - **Markus Erik Sügis** - 
    [sygism](https://github.com/sygism)

## License

This project is not licensed and is free to be used in any way.
