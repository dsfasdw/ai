# Portfolio Website with AI Chatbot

A modern, responsive portfolio website featuring an integrated AI chatbot powered by Groq.

## Features

- **Modern Portfolio Design**
  - Hero section with gradient background
  - About, Skills, Projects sections
  - Responsive design for all devices
  - Smooth scrolling navigation

- **AI Chatbot Integration**
  - Powered by Groq API
  - Multiple model support (Llama, Mixtral, Gemma)
  - Real-time chat interface
  - Local API key storage
  - Conversation history management

## Files

- `index.html` - Main portfolio page
- `styles.css` - Styling and responsive design
- `script.js` - Chatbot functionality and interactions
- `config.js` - **Configuration file - Add your API key here**
- `chat.py` - Original Python chatbot (reference)

## How to Use

1. **Open the Portfolio**
   - Simply open `index.html` in your web browser
   - No server required - works locally!

2. **Set Up the Chatbot**
   - Open `config.js` file
   - Replace `YOUR_API_KEY_HERE` with your actual Groq API key
   - Get your free API key from https://console.groq.com/keys
   - Save the file and refresh the page
   - The chatbot will work directly!

3. **Customize Your Portfolio**
   - Edit `index.html` to update:
     - Your name and title
     - About section content
     - Skills and projects
     - Contact information
   - Modify `styles.css` to change colors and styling

## Customization

### Change Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
}
```

### Update Personal Information
Edit the content in `index.html`:
- Hero section: Name, title, description
- About section: Your story
- Skills: Your expertise
- Projects: Your work
- Contact: Your social links

## API Key Security

- The API key is stored in `config.js` file
- It's never sent to any server except Groq's API
- **Important:** Don't commit `config.js` to public repositories if it contains your API key
- Add `config.js` to `.gitignore` if using version control

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge
- Firefox
- Safari
- Opera

## Notes

- The chatbot requires an active internet connection
- API key must be valid and have access to Groq models
- Rate limits apply based on your Groq API plan

## License

Free to use and modify for personal or commercial projects.

