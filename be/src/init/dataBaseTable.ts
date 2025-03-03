export const initData = {
  "chat": [
    "id INT AUTO_INCREMENT PRIMARY KEY",
    "user VARCHAR(255)",
    "userId INT",
    "messageId INT NOT NULL",
    "title VARCHAR(255) NOT NULL DEFAULT 'untitled'",
    "isDelete BOOLEAN NOT NULL DEFAULT FALSE",
    "creationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP",
    "modificationTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP"
  ]
}
