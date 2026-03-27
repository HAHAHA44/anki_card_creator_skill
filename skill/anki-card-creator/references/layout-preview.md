# Layout Preview Reference

Use the ASCII preview below whenever presenting the default card layout to the user. Copy it verbatim into your response — do not paraphrase or summarise it.

## Default Layout

```
+-------------------------------------+
|  FRONT (shown as question)          |
|                                     |
|  [Context]   <- topic cue (if set) |
|  [Prompt]    <- main prompt        |
|  [Example]   <- example (if set)   |
+-------------------------------------+

+-------------------------------------+
|  BACK (shown after reveal)          |
|                                     |
|  [Answer]    <- answer             |
|  [*] [Extra] <- extra (if set)     |
+-------------------------------------+
```

## Default Field Lists

- `front_layout`: context, prompt, example
- `back_layout`: answer, extra

## Extra Field Rendering Rule

The `extra` field always renders with a "[*]" prefix (displayed as the special marker) on whichever side it appears. This marker is fixed and not user-configurable.

## Changing The Layout

If the user wants to move a field:

1. Remove it from its current side.
2. Add it to the other side.
3. Update `front_layout` and `back_layout` in `## Card Layout` of the deck spec.

Valid field names: `prompt`, `answer`, `context`, `example`, `extra`.

A field may only appear on one side. The same field cannot be in both `front_layout` and `back_layout`.
