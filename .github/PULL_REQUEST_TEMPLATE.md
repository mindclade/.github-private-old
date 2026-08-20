## Member experience

Describe what changes for organization members and which links, operating guidance, or
repository boundaries are affected.

## Information safety

- Data classification: internal / confidential / restricted
- Sensitive operational detail introduced: none / describe
- Security, privacy, customer-data, model-weight, or biosecurity impact: none / describe

## Validation evidence

List the exact commands run and their results.

```text
make validate
make lint
```

## Checklist

- [ ] The profile remains useful to every organization member, including new starters and on-call responders.
- [ ] Every linked repository or runbook exists and its audience can access it.
- [ ] No credential, customer data, private model material, restricted biological content, or incident-sensitive detail is present.
- [ ] `.github-private` remains private and `profile/README.md` remains the rendered source.
- [ ] Workflow permissions are explicit and every external action is immutable-pinned.
