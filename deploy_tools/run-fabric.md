Use this command to run the fabric deployment script:

To deploy to the staging server

```bash
fab deploy -i ../aws/ListsWebsite.pem -H ubuntu@superlists-1234-staging.xyz
```

To deploy to the live server

```bash
fab deploy -i ../aws/ListsWebsite.pem -H ubuntu@superlists-1234.xyz
```
