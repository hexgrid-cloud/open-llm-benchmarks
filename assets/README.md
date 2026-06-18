# assets/

Charts and images for each benchmark article, one folder per article slug:

```
assets/<gpu>-<model>-<precision>-<engine>/
```

The article references images with a relative path, e.g.
`![...](../assets/rtx5090-qwen3.5-9b-bf16-vllm/sweep.png)`.

Commit the actual PNGs here (don't hotlink Reddit/imgur — those links rot and you lose
the images). In-repo images render on GitHub and survive forever.
