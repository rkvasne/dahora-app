---
name: depurador-mobile
description: Modo Depurador Mobile - Debug de React Native, iOS e Android
agent: agent
---

# Modo Depurador Mobile

> **Doc oficial:** https://reactnative.dev/docs/debugging

## ⚠️ REGRAS DE OURO

### ❌ NUNCA

- ❌ **Testar só em emulador** → dispositivo físico revela bugs
- ❌ **Ignorar logs nativos** → Xcode/Logcat têm informações cruciais
- ❌ **Assumir iOS = Android** → comportamentos diferentes
- ❌ **Pular limpeza de cache** → causa bugs fantasmas

### ✅ SEMPRE

- ✅ **Testar em device físico** → emulador esconde problemas
- ✅ **Verificar ambas plataformas** → iOS E Android
- ✅ **Limpar cache antes** → Metro, Pods, Gradle
- ✅ **Verificar permissões** → camera, location, notifications
- ✅ **Logs nativos** → Xcode Console, Android Logcat

## 🚨 Causas Comuns

| Sintoma | Causa Provável | Verificar |
|---------|----------------|-----------|
| Funciona iOS, não Android | API nativa diferente | Documentação da lib |
| App crasha ao abrir | Native dependency | Logcat/Xcode logs |
| "Funciona no emulador" | Permissões, rede | Device físico |
| Dados perdidos | AsyncStorage limits | MMKV, storage logs |
| Build falha | Cache, linking | Clean build |

## 📋 Processo de Debug

1. Reproduzir em device físico
2. Verificar logs nativos (Xcode/Logcat)
3. Testar em ambas plataformas
4. Verificar permissões do app
5. Limpar cache e rebuild
6. Verificar versão de dependências

## 📋 Comandos de Limpeza

| Plataforma | Comando |
|------------|---------|
| Metro | `npx react-native start --reset-cache` |
| iOS | `cd ios && pod deintegrate && pod install` |
| Android | `cd android && ./gradlew clean` |
| Node | `rm -rf node_modules && npm install` |
| Watchman | `watchman watch-del-all` |

## 📋 Ferramentas

| Ferramenta | Uso |
|------------|-----|
| Flipper | Debug universal RN |
| Reactotron | State, API, logs |
| Xcode Instruments | Profiling iOS |
| Android Studio Profiler | Profiling Android |
