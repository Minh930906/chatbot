ChatBot
## API Reference

#### Send message

```http
  POST /chat/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message_text` | `string` | **Required**. Message to ChatBot |

this endpoint has rate limiting which is only afford the user to call it 3 times per minutes

#### Get chat history

```http
  GET /chat_history
```

It's public,no need authorization

#### Register user

```http
  POST /register
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Required**. Email to register |
| `username` | `string` | **Required**. Username to register |
| `password` | `string` | **Required**. password to register |

#### Login for access token

```http
  POST /token
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. For token |
| `password` | `string` | **Required**. For token |

Response
 key | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `access_token` | `string` |token we get |
| `token_type` | `string` | type of toke |

## FYI

In requirements.txt packages included to project, but it still some contains unnecessary packages


## Authors

- [@Miki](https://www.github.com/Minh930906)
