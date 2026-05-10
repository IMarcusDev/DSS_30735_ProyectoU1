<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped src="../styles/header.css"></style>

<template>
    <header>
        <router-link to="/" class="logo">
            <img src="/logo.png" alt="logo de SecureFrames Gallery">
            <h1>SecureFrame Gallery</h1>
        </router-link>
        <h3>Somos una aplicación de galería para almacenar imagenes de manera segura</h3>
        <div>
            <button type="button" @click="router.push('/login')">Iniciar Sesión</button>
            <button type="button" @click="router.push('/register')">Registrarse</button>
        </div>
    </header>
</template>
