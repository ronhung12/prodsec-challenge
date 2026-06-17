# AI Tools Usage
-If you used AI, where did you use it and why?
```
I used Codex to help me 
    1. Create custom Semgrep rules in semgrep.yml
    2. Update the security.yml file to include a Test stage in the CI
    3. Analyze the semgrep results locally

I used Google Search (gemini) to search up information about:
    1. HS256
    2. verify_exp parameter
```
-What did it get right?

```It was incredibly accurate in creating a working Test stage that had the proper envinronment setup, semgrep scanner, and script to block on the Semgrep results```

What did it get wrong or miss?

```The AI did a second passthrough of the codebase with the Semgrep results and it did not find the HS256 vulnerability and that the test cases contained live user credentials.```

How did you verify or challenge the output?

```I always read over AI-generated code, read its reasoning to make sure the logic flows, and will have AI validate itself by running either in a sandbox or creating test cases.```

Did it change your CI design, custom rule, or triage decision?

```It changed my CI design and custom rules.```

If you did not use AI, where do you think AI would and would not be useful in this workflow?

 ``N/A``