# Master SK Academy Website

A modern, responsive website for Master SK Academy - a Tamil Nadu State Board coaching center located in Vellore.

## Features

- ✅ Fully responsive design (mobile, tablet, desktop)
- ✅ Clean, professional education-themed UI
- ✅ Smooth scrolling and animations
- ✅ Mobile hamburger menu
- ✅ SEO-friendly structure
- ✅ Easy to edit content
- ✅ No frameworks required (pure HTML, CSS, JavaScript)

## Color Theme

- **Primary Color**: Dark Blue (#1a365d)
- **Secondary Color**: Yellow/Gold (#fbbf24)
- **Background**: Light Gray (#f5f5f5)

## File Structure

```
├── index.html          # Home page
├── about.html          # About Us page
├── courses.html        # Courses page
├── admissions.html     # Admissions page
├── contact.html        # Contact page
├── styles.css          # Main stylesheet
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Pages Overview

### 1. Home Page (index.html)
- Hero section with academy name and tagline
- Highlights section (6 key features)
- Quick info about SSLC and HSC coaching
- Call-to-action buttons

### 2. About Us (about.html)
- Academy description
- Teaching philosophy
- Experience and success metrics
- Why choose us section

### 3. Courses (courses.html)
- SSLC (Class X) courses: Maths, Science, Social, Tamil, English
- HSC (Class XII) Science Group: Physics, Chemistry, Maths, Biology/CS
- HSC (Class XII) Commerce Group: Accountancy, Commerce, Economics, Business Maths/CS
- Coaching methodology section

### 4. Admissions (admissions.html)
- Admission process details
- Course information
- Class timings
- Required documents
- Fee structure information
- Inquiry/Registration form

### 5. Contact (contact.html)
- Phone number, email, and location
- Contact form
- Office hours
- Map placeholder (for Google Maps integration)

## Customization Guide

### 1. Update Contact Information

**In contact.html:**
- Replace `+91 XXXXXXXXXX` with your actual phone number
- Replace `info@masterskacademy.com` with your actual email
- Update the address in the location section
- Update office hours if needed

**In index.html footer:**
- Update contact information in the footer section

### 2. Update Colors (Optional)

**In styles.css:**
Edit the CSS variables at the top of the file:
```css
:root {
    --primary-color: #1a365d;      /* Dark Blue */
    --secondary-color: #fbbf24;    /* Gold/Yellow */
    --accent-color: #2563eb;        /* Lighter Blue */
    --bg-color: #f5f5f5;            /* Light Gray */
}
```

### 3. Add Logo Image

Replace the text logo with an image:
1. Add your logo image to the project folder
2. In all HTML files, replace:
```html
<div class="logo">MSK</div>
```
with:
```html
<img src="your-logo.png" alt="Master SK Academy Logo" class="logo-image">
```
3. Update CSS for `.logo` class to style the image

### 4. Add Google Maps

**In contact.html:**
Replace the map placeholder with Google Maps embed code:
```html
<iframe 
    src="YOUR_GOOGLE_MAPS_EMBED_URL"
    width="100%" 
    height="400" 
    style="border:0;" 
    allowfullscreen="" 
    loading="lazy">
</iframe>
```

### 5. Connect Forms to Backend

**In script.js:**
The forms currently show alert messages. To connect to a backend:

1. Replace the form submission handlers in `script.js`
2. Use fetch API or form action to send data to your server
3. Example:
```javascript
fetch('your-backend-endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
})
```

### 6. Update Content

All content is easy to edit directly in the HTML files:
- Text content: Edit directly in HTML
- Course descriptions: Update in `courses.html`
- About section: Update in `about.html`
- Admission details: Update in `admissions.html`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment

### Option 1: Static Hosting
Upload all files to any static hosting service:
- GitHub Pages
- Netlify
- Vercel
- AWS S3
- Any web hosting service

### Option 2: Local Server
For testing locally:
```bash
# Using Python
python -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

## SEO Features

- Meta descriptions on all pages
- Semantic HTML structure
- Proper heading hierarchy (h1, h2, h3)
- Alt text ready for images (when you add them)
- Clean URL structure
- Mobile-friendly (important for SEO)

## Performance Tips

1. **Optimize Images**: When adding images, compress them before uploading
2. **Minify CSS/JS**: For production, consider minifying CSS and JS files
3. **Add Favicon**: Add a favicon.ico file in the root directory
4. **Enable Compression**: Enable gzip compression on your server

## Future Enhancements (Optional)

- Add image gallery
- Add testimonials section
- Add blog/news section
- Add online payment integration
- Add student portal
- Add live chat widget
- Add social media links
- Add Google Analytics

## Support

For questions or customization help, refer to the code comments in each file. All files are well-commented for easy understanding.

## License

This website template is created for Master SK Academy. Customize as needed for your use.

---

**Note**: Remember to update all placeholder content (phone numbers, emails, addresses) before going live!

