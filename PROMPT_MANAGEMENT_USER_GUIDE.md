# LLM Prompt Management - User Guide

## Quick Start

You now have a fully functional LLM Prompt Management System! Here's how to use it.

### Accessing the Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/bank/llmprompt/`
2. You'll see all configured prompts

### Current Default Prompts

Two default prompts are already created:

1. **MCQ Prompt** - Used to generate multiple choice questions
2. **Descriptive Prompt** - Used to summarize articles for study notes

Both are marked as active and default.

## How to Manage Prompts

### Adding a New Prompt

1. Click **"Add LLM Prompt"** button in top right
2. Fill in the form:
   - **Source URL** (optional): Leave empty for global/default prompt, or enter a URL for source-specific prompts
   - **Prompt Type**: Choose either 'MCQ' or 'Descriptive'
   - **Prompt Text**: Enter your prompt. You can use `{title}` and `{content}` placeholders
   - **Is Default**: Check this if this should be the fallback for this prompt type
   - **Is Active**: Check to enable the prompt

3. Click **Save**

### Example: Creating a Source-Specific MCQ Prompt

1. Click **Add LLM Prompt**
2. Fill in:
   - Source URL: `https://example-news.com`
   - Prompt Type: MCQ
   - Prompt Text:
     ```
     You are an expert creating MCQs for banking exams.
     Focus on topics from: {title}
     Article: {content}
     
     Generate 5 MCQs in JSON format:
     {
         "questions": [
             {
                 "question": "...",
                 "option_a": "...",
                 "option_b": "...",
                 "option_c": "...",
                 "option_d": "...",
                 "correct_answer": "A",
                 "explanation": "..."
             }
         ]
     }
     ```
   - Is Default: Unchecked (since it's for a specific source)
   - Is Active: Checked

3. Click **Save**

### Editing an Existing Prompt

1. Click on the prompt in the list
2. Edit the fields as needed
3. Click **Save**
4. Changes take effect immediately!

### Disabling a Prompt (without deletion)

1. Click on the prompt
2. Uncheck **Is Active**
3. Click **Save**

The prompt stays in database for history but won't be used.

### Deleting a Prompt

If you absolutely must delete:
1. Click on the prompt
2. Click **Delete** button at bottom
3. Confirm deletion

## How Prompts Are Selected

When the system generates MCQs or Descriptive content, it follows this priority:

1. **First**: Check for source-specific prompt
   - Example: If processing article from `https://example.com/news`, look for prompt with that exact source URL

2. **Second**: Use default prompt for that type
   - Example: Default MCQ prompt if no source-specific found

3. **Third**: Fallback to hardcoded prompt in Python code
   - Always available as last resort

## Prompt Template Placeholders

You can use these placeholders in your prompts:

- `{title}` - Will be replaced with the article title
- `{content}` - Will be replaced with the article body

Example:
```
Title: {title}
Content: {content}
```

## Best Practices

### 1. Always Have a Default
- Keep at least one default MCQ and one default Descriptive prompt
- This ensures the system always works

### 2. Use Meaningful Source URLs
- Use full URLs for consistency: `https://example.com/news`
- Consider your source structure when assigning prompts

### 3. Test New Prompts
- After creating a new prompt, test it with actual content
- Check that the generated output is what you expect

### 4. Keep Defaults General
- Make default prompts flexible to work with any article
- Use source-specific prompts for specialized needs

### 5. Clear Placeholders
- Always use `{title}` and `{content}` exactly as shown
- Don't use other placeholder formats

## Troubleshooting

### Prompt Not Being Used
- Check if it's marked as **Active**
- Verify the source URL matches exactly (if source-specific)
- Check that the correct **Prompt Type** is selected

### Format Errors in Generated Content
- Verify your prompt includes the JSON structure
- Check that placeholders are correctly escaped
- Test the prompt directly in admin interface

### Cannot Add More Than One Default
- The system enforces only one default per (source_url, prompt_type)
- If you try to set a new default, the old one will be unset automatically

## System Status

✅ **Migration Applied**: Database schema created
✅ **Default Prompts Created**: MCQ and Descriptive ready to use
✅ **Admin Interface**: Fully functional
✅ **Integration**: CurrentAffairsProcessor fetches prompts from database
✅ **Fallback Logic**: Hardcoded prompts as final fallback

## Technical Details

- **Model**: `bank.models.LLMPrompt`
- **Admin**: `bank.admin.LLMPromptAdmin`
- **Processor**: `genai.tasks.current_affairs.CurrentAffairsProcessor`
- **Database Table**: `bank_llmprompt`

## Support

If you need to create custom prompts for different content types, the system is designed to be flexible. You can:

1. Create source-specific prompts for different news sources
2. Create specialized prompts for different exam types
3. Mix and match generic and specific prompts

The system automatically selects the most specific prompt available!
