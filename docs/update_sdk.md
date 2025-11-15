# 🧩 SDK Update Manual — Evolution Client Integration

Este documento descreve o processo **seguro e manual** para atualizar a versão do pacote  
`evolution-client` usado pelo projeto **sebrae-worker**.

---

## 🔧 1️⃣ Verificar versão mais recente do SDK

O SDK está hospedado no GitHub:
👉 [https://github.com/Maquina-Digital/evolution-client-py-sdk](https://github.com/Maquina-Digital/evolution-client-py-sdk)

Para ver as versões disponíveis:

```bash
git ls-remote --tags https://github.com/Maquina-Digital/evolution-client-py-sdk.git

A saída mostrará algo como:

91211b2f8e58e0733a3c8ea7f7fa456910de6afc        refs/tags/v1.0.0
a0b7e3ef9918dd287e04620d5b2b5b8b8cd67421        refs/tags/v1.1.0

🧱 2️⃣ Atualizar o pyproject.toml

No projeto sebrae-worker, abra o arquivo pyproject.toml e altere a linha:

evolution-client = { git = "https://github.com/Maquina-Digital/evolution-client-py-sdk.git", tag = "v1.0.0" }


para apontar para a nova versão, por exemplo:

evolution-client = { git = "https://github.com/Maquina-Digital/evolution-client-py-sdk.git", tag = "v1.1.0" }

📦 3️⃣ Atualizar dependências localmente

Execute os seguintes comandos no terminal, dentro do ambiente Poetry:

poetry lock --no-cache
poetry install


Esses comandos irão:

Atualizar o arquivo poetry.lock;

Instalar a nova versão do SDK no ambiente de desenvolvimento.

🧪 4️⃣ Rodar testes e validar integração

Antes de fazer o push:

make test


Confirme que:

Os testes relacionados ao SDK passam (pytest -k evolution_client);

O container sebrae_test_runner está saudável.

🚀 5️⃣ Comitar e publicar

Se tudo estiver OK:

git add pyproject.toml poetry.lock
git commit -m "chore: bump evolution-client SDK to v1.1.0"
git push origin main


Isso acionará automaticamente:

O GitHub Action que faz o build e push da nova imagem Docker multi-arch;

O Portainer, que pode puxar a nova imagem ao atualizar o stack.

🧩 6️⃣ Verificar o deploy

Após o pipeline completar:

Acesse o Portainer;

Abra o stack do Sebrae Worker;

Verifique o log de inicialização e confirme que o SDK está na versão esperada.

🧠 Dica de ouro

Sempre incremente a versão do SDK com tags semânticas:

v1.0.x → correções;

v1.x.0 → novas features compatíveis;

v2.0.0 → mudanças quebrando compatibilidade.