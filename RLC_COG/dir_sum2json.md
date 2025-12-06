Let's do one thing at a time before we can continue we first must get `file2sum(cwfd + "/RLC_COG.ui"))` to output a summary of `RLC_COG.ui` based on the output of of a api call, in the style of `strawberry_test()`, however we want to make it think there was a user assistant interaction where the user asked for a markdown code escaped 111 chars or less summary of `test.c` in  and the assistant replied with a "think" block follwoed by answer and in markdown \`\`\` quoted text.

```python
import requests
  import json
  import os

  url = "https://openrouter.ai/api/v1/chat/completions"
  headers = {
      "Authorization": f"Bearer {os.environ.get('OPENROUTER_API_KEY')}",
      "Content-Type": "application/json"
  }
  payload = {
"model": "openai/gpt-oss-20b",
"messages": [
  {
    "role": "system",
    "content": "role: you are a junior level engineer, preparing short summaries of files in a large project"
  },
  {
    "role": "user",
    "content": "in 111 chars or less summarize the following file:\n```\n#include<stdio.h>\n#include<math.h>\n\nint main() {\n    float a, b, c, determinant, r1, r2, real, imag;\n    printf(\"\\n\\nEnter coefficients a, b and c: \\n\\n\\n\");\n    scanf(\"%f%f%f\", &a, &b, &c);\n\n    determinant == b*b - 4*a*c; \n    if (determinant > 0) {\n        r1 = (-b + sqrt(determinant))/2*a;\n        r2 = (-b - sqrt(determinant))/2*a;\n        printf(\"\\n\\n\\nRoots are: %.2f and %.2f \", r1, r2);\n    } else if (determinant == 0) {  \n        r1 = r2 = -b/(2*a);\n        printf(\"\\n\\n\\nRoots are: %.2f and %.2f \", r1, r2);\n    } else {\n        real = -b/(2*a);\n        imag = sqrt(-determinant)/(2*a);\n        printf(\"\\n\\n\\nRoots are %.2f + i%.2f and %.2f - i%.2f \", real, imag, real, imag);\n    }\n    return 0;\n}\n```"
  },
  {
    "role": "assistant",
    "content": "summary:\n\n```C program to calculate and display real or complex roots of a quadratic equation using coefficients.```",
    "refusal": null,
    "reasoning": "The user requested a concise summary of a C program. The program reads coefficients of a quadratic equation, computes the determinant, and based on its value, calculates and prints either two real roots, one repeated real root, or two complex roots. The assistant generated a short summary that captures this functionality within the character limit."
  }
]
}

  response = requests.post(url, headers=headers, json=payload)
  print(response.json())
```

### Currently works!

`dir2tree_data()` looks in the top level of `dir_path` for a file `cog_cfg.json` and parse for a `gignore` var containing a `.gitignore` style list of files and dirs to ignore and ignore them.

gignore json:

```json
    "gignore": ".git/\n*.key"
```

### Why this works:
- `.git/` → ensures the entire Git directory is ignored.
- `*.key` → ignores any file ending in `.key`.
- Stored as a single string with newline separators, so later we can split and feed it into a glob matcher.

This way, our config mirrors the semantics of a real `.gitignore` file.
