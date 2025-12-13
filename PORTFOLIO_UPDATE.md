# How to Update Portfolio Information in the Chatbot

The chatbot automatically knows about your portfolio! To update the information, edit the `portfolioInfo` object in `script.js`.

## Location
Open `script.js` and find the `portfolioInfo` object (around line 25).

## What to Update

### 1. Personal Information
```javascript
name: 'Your Name',  // Change to your actual name
title: 'Full Stack Developer & AI Enthusiast',  // Your job title
description: 'I create beautiful, functional websites...',  // Your tagline
```

### 2. About Section
```javascript
about: [
    'Your first paragraph about yourself...',
    'Your second paragraph...'
],
```

### 3. Statistics
```javascript
stats: {
    projectsCompleted: '50+',  // Your number
    yearsExperience: '3+',       // Your experience
    clientSatisfaction: '100%'   // Your satisfaction rate
},
```

### 4. Skills
Add or modify skills:
```javascript
skills: [
    {
        name: 'Python',
        description: 'Backend development, AI/ML, Automation'
    },
    // Add more skills here
],
```

### 5. Projects
Add or modify projects:
```javascript
projects: [
    {
        name: 'AI Chatbot',
        description: 'Description of your project...'
    },
    // Add more projects here
],
```

### 6. Contact Information
```javascript
contact: {
    email: 'your.email@example.com',
    github: 'github.com/yourusername',
    linkedin: 'linkedin.com/in/yourprofile'
}
```

## After Updating

1. Save `script.js`
2. Refresh your browser
3. The chatbot will now know all the updated information!

## Important Notes

- The chatbot uses this information to answer questions about you
- Make sure the information matches what's on your portfolio website
- You can add as many skills and projects as you want
- The chatbot will automatically include all this information in its responses

