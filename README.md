<h1 align="center">Network</h1>
<h3 align="center"><a href="https://network.applikuapp.com">network.applikuapp.com</a></h3>

<br/>

<br/>

<h2>About this Project</h2>
<p>This meticulously crafted forum web app serves as a testament to my abilities, offering a large array of features. I invite you to experience the application as a demo user.</p>
<p>This website was crafted with the intention to have it contain the principal features of social media apps like Reddit, Instagram, Twitter, and Facebook. Initially, SoNet was going to be a simple clone one of the listed apps, however, I wanted to be more creative with the process. 
Eventually, it evolved into it's own unique app.</p>
<p>The construction of this project required the following tools<p>
<ul> 
    <li>Python</li>
    <li>Django</li>
    <li>JavaScript</li>
    <li>SQLite</li>
    <li>PostgreSQL</li>
    <li>HTML</li>
    <li>CSS</li>
    <li>SASS</li>
    <li>Boostrap</li>
</ul>

<h3>Front End:</h3>
<p>The frontend of the project was developed using a combination of programming languages and tools, including <b>JavaScript, HTML, SASS, CSS, and Bootstrap</b>. To tackle this more complex project, I made a deliberate decision to concentrate on <b>JavaScript</b> in order to deepen my understanding of its core principles and concepts. This choice allowed me to significantly improve my <b>JavaScript</b> proficiency, as I was forced to expand my knowledge.</p>
<p>In addition to <b>JavaScript</b>, I also integrated <b>SASS</b> into the project. The reason for this was its more readable and concise syntax compared to standard <b>CSS</b>, which made managing styles considerably easier. The adoption of <b>SASS</b> improved the overall maintainability of the project's stylesheets, contributing to a more efficient development process.</p>
<p>To ensure the frontend's responsiveness and a polished appearance, I decided to utilize the <b>Bootstrap</b> framework. This choice allowed me to create layouts that adapt seamlessly to different screen sizes and maintain a professional and refined look. By combining <b>JavaScript, HTML, SASS, CSS,</b> and <b>Bootstrap</b>, I successfully crafted a frontend that met the project's requirements and provided me with valuable experience in these essential web development technologies.</p>

<h3>Back End:</h3>
<p>The backend was constructed with the following array of technologies and tools: <b>Python, Django, SQLite, and PostGreSQL.</b> The language of choice for the back end was <b>Python</b> due to it's extensive libraries and it's straightforward syntax. This decision laid the foundation for our backend development journey. </p>

<p>After committing to <b>Python</b>, the next crucial choice was between two robust web frameworks: <b>Flask and Django.</b> Given the scalability requirements inherent to a social media application, I opted for <b>Django</b>, a choice that allowed us to delve into the intricate world of Django models, settings, URLs, and functions. This strategic selection paved the way for a more streamlined and feature-rich backend system.</p>

<h3>Installation and Deployment:</h3>
<p>If you would like to take this project and copy it for personal use, you can following the following guide:
    <ol>
        <li>Fork the project</li>
        <li>Go to the requirements.txt file and pip install all of those requirements</li>
        <li>Create a '.env' file in the root directory
            <ul>
                <li>Create a variable titled "DATABASE_URL" with the database that you would like to link to the app</li>
                <li>Create a variable titled "DJANGO_SECRET_KEY" with your secret key</li>
                <li>If you're going to deploy the app, create a variable titled "DJANGO_ALLOWED_HOSTS" with the allowed domains you would like to deploy to</li>
            </ul>
        </li>
        <li>Go to settings.py and change "DEBUG" to "True"</li>
        <li>Run the command "python3 manage.py makemigrations"</li>
        <li>Run the command "python3 manage.py migrate" to migrate the Django models to the database</li>
        <li>If you would like to make changes to the SASS file, you can download "Live SASS Compiler" for VSCode to automatically convert SASS changes to CSS</li>
        <li>Run "python3 manage.py runserver" to start the server</li>
    </ol>
The project contains all of the proper files for it to be deployed on Heroku. It only requires you switch "DEBUG" in settings.py to "False" before creating a heroku app and deploying the forked repository.
</p>


