<template>
  <!-- this is the settigs page for the user, mainly for them to see who they are logged in as
   and to log out or delete their account if needed -->
    <h1 class="mb-4 text-center">Settings</h1>
  <!-- using the user store display the users username -->
    <h3 class="mb-3 alert alert-info text-center">Logged In User: {{ loggedinuser.username }}</h3>
    <p class="mb-3 alert alert-dark text-center">FirstWheels App Built By: Munaib Ishaq</p>

    <!-- logout button -->
    <button class="btn btn-dark mt-5 w-100" @click="loguserout">Logout</button>
    <!-- delete acc button -->
    <button @click="confirmDelete" class="btn btn-danger mt-4 w-100">Delete Your Account</button>

  </template>
  
  <script>
  import { useUserStore } from '@/stores/user'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  
  export default {
    setup()
    { // access the user store
      // get the router
      const loggedinuser = useUserStore()
      const menu = useRouter()
      return { loggedinuser, menu }
    },
      
    methods:
    {
      loguserout()
      { // if user wants to logout then use user store to log them out
        this.loggedinuser.logoutuser()
        // go to the login page
        this.menu.push('/login')
      },
  
      async confirmDelete() // delete account
      {
        // confirm the user wants to delete their account
        if (confirm("You Have Chosen To Delete This Account, Are You Sure?")) {
          try {
            // sent use details to the delete user api endpoint
            await axios.delete('/user/del/', { headers: {Authorization: "Token "+this.loggedinuser.token}})
            // also log user out of the frontend
            this.loggedinuser.logoutuser()
            // go to login
            this.menu.push('/login')
          } 
          // error checking
          catch (usererror) {alert("We Could Not Delete This Account, Try Again Later")}
        }
      },
      
    },
  }
  </script>
