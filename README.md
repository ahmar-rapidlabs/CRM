
# Customer Relationship Management

CRM helps us keep track of projects by matching them with team’s available time and skills, making sure to deliver AI solutions efficiently and on time.


## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)


## Installation

To run this project on your local machine, follow the steps below:

### Prerequisites

Please mae sure that you have installed the following on your local machine.

- Python 3.9.0 or higher
- Node.js v16.5.0 or higher
- npm 6.14.9 or higher

#### 1. Clone Repository

```bash
https://github.com/ahmar-rapidlabs/CRM.git
```
#### 2. Backend

Navigate to server directory
```bash
cd server
```
Create and activate Virtual Envireonment (windows)
```
python -m venv env
.\env\Scripts\activate
```
Create and activate Virtual Envireonment (Linux and MacOS)
```
python -m venv env
source env/bin/activate
```
Install Dependencies
```bash
pip install -r requirements.txt
```
Run Django server on port 8000
```
python manage.py runserver
```
#### 3. Client
Navigate to client directory
```
cd client
```
Install Dependencies
```
npm install
```
Run React server on port 3000
```
npm start
```
Now, the backend will launch on `localhost:8000` and client will run on `localhost:3000`. make sure you have allowed `cors` in your browser.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SECRET_KEY`




## Tech Stack

**Client:** React, Redux, TailwindCSS

**Server:** Django


## Used By

This project is used by the following companies:

- Rapid labs


## Authors

- [@ahmar-rapidlabs](https://github.com/ahmar-rapidlabs)
- [@osman-y](https://github.com/osman-y)


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## Support

For support, email info@rapidlabs.ai or join our Slack channel.

