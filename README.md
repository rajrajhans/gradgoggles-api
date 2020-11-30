<p align="center">
  <a href="https://gradgoggles.com">
    <img alt="GradGoggles" src="http://assets.rajrajhans.com/gg_compressed.png" width="250"/>
  </a>
</p>
<h1 align="center">
  <a href="https://gradgoggles.com">GradGoggles</a> API
</h1>
Gradgoggles is a virtual yearbook and scrapbook application developed using Flask (API), ReactJS and Android.

---
<p align="center">
  <a href="https://gradgoggles.com" target="_blank">
    <img alt="website_up" src="https://img.shields.io/badge/Website-Up-<COLOR>.svg?style=flat" width="100"/>
  </a>

  <a href="https://play.google.com/store/apps/details?id=com.team.android.gradgoggles&hl=en" target="_blank">
    <img alt="GradGoggles" src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" width="100"/>
  </a>
</p>


---

This repo contains the source code for GradGoggles API developed using Flask in Python. The GG WebApp and Android app both use this API. 

### Functionalities implemented in the API -

- Create, Read, Update, Search, Delete users, their details, and their scraps.
- JWT based Authentication. 
- Email address verification using Timed Serializer Tokens. Uses Sendgrid to actually send the emails. 
    - The timed serialized tokens are also used for the "Forgot Password" functionality.
- Client side file upload to s3 using signed requests. (Check [this](https://rajrajhans.com/2020/06/2-ways-to-upload-files-to-s3-in-flask/) for more details)
- Pagination for `/users` endpoint response. 

The `/tests` folder contains some unit tests to ensure the critical functionalities of the codebase do not break. You can run all tests using `python -m pytest` 

For more details and source code for the GradGoggles WebApp and the Android app, check out [this repository](https://github.com/rajrajhans/gradgoggles).   

### Running the api locally 

In the project directory, you can run:

#### `python app.py`

Runs the app in the development mode.\
Open [http://localhost:5000](http://localhost:5000) to view it in the browser.

### To know more about GradGoggles, [read this blog post on rajrajhans.com](https://rajrajhans.com/2020/08/casestudy-gradgoggles/) or visit  [this repository](https://github.com/rajrajhans/gradgoggles).