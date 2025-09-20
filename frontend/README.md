# Next.js Authentication Project

## Overview
This repository showcases my work on a full-stack authentication system built with **Next.js**, following Hitesh Choudhary's [Next.js Course](https://www.youtube.com/watch?v=eaQc7vbV4po). It includes user sign-up, login, profile management, and email verification, forgot password.

## Features
- User authentication
- Email verification using Mailtrap
- MongoDB with Mongoose for data storage
- TypeScript for type-safe coding

## Tech Stack
- Next.js (App Router)
- TypeScript
- MongoDB (Mongoose)
- NodeMailer (Mailtrap)
- React Hot Toast

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kamlesh0928/nextjs-auth.git
   cd my-app
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the root directory with:
   ```env
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
   TOKEN_SECRET=<your-token-secret>
   MAILTRAP_USER=your-mailtrap-user-here
   MAILTRAP_PASS=your-mailtrap-pass-here
   DOMAIN=<your-domain-url-or-http://localhost:3000>
   ```

4. **Run Locally**:
   ```bash
   npm run dev
   ```
   Visit `http://localhost:3000` to see the app.

## Acknowledgments

- **Hitesh Choudhary**: For the detailed and engaging [Next.js tutorial](https://www.youtube.com/watch?v=eaQc7vbV4po) that made learning fun and practical.

