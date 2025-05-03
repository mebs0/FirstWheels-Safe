<script setup>
import { useUserStore } from '@/stores/user'
const user = useUserStore()
// this is the main app file where we setup the router
</script>

<template>
  <div class="app-wrapper">
    <router-view />
    <!-- crreate the navbar for the main menu bar at the bottom -->
    <nav class="navbar bg-dark fixed-bottom navbar-dark">
      <div class="container justify-content-around">

        <!-- link for the lookup page -->
        <router-link to="/" class="text-center">
          <i class="bi bi-search" id="iconsizing"></i>
          <div id="namesizing">Lookup</div>
        </router-link>

        <!-- link for the garage page -->
        <router-link
          to="/garage" class="text-center"
          :class="user.hasloggedin ? 'text-light' : 'text-secondary'"
          :style="{ pointerEvents: user.hasloggedin ? 'auto' : 'none' }">
          <!-- above greys out icon if user isnt logged in -->

          <i class="bi bi-tools" id="iconsizing"></i>
          <div id="namesizing">Garage</div>
        </router-link>

        <!-- link for the checklist page -->
        <router-link
          to="/checklist" class="text-center"
          :class="user.hasloggedin ? 'text-light' : 'text-secondary'"
          :style="{ pointerEvents: user.hasloggedin ? 'auto' : 'none' }">
          <!-- above greys out icon if user isnt logged in -->

          <i class="bi bi-card-checklist" id="iconsizing"></i>
          <div id="namesizing">Checklist</div>
        </router-link>

        <!-- link for the settings page -->
        <router-link
          to="/settings" class="text-center"
          :class="user.hasloggedin ? 'text-light' : 'text-secondary'"
          :style="{ pointerEvents: user.hasloggedin ? 'auto' : 'none' }">
          <!-- above greys out icon if user isnt logged in -->

          <i class="bi bi-gear" id="iconsizing"></i>
          <div id="namesizing">Settings</div>
        </router-link>

        <!-- link for the login page -->
        <router-link
          to="/login" class="text-center"
          :class="!user.hasloggedin ? 'text-light' : 'text-secondary'"
          :style="{ pointerEvents: !user.hasloggedin ? 'auto' : 'none' }">
          <!-- above greys out icon if user is logged in -->

          <i class="bi bi-person" id="iconsizing"></i>
          <div id="namesizing">Login</div>
        </router-link>

      </div>
    </nav>
  </div>
</template>

<style>
#iconsizing{
  font-size: 1.52rem;
}
#namesizing{
  font-size: 0.76rem;
}
</style>