// This is the pinia store, its used to manage the users state, tracking their username and login token to help authenication
import { defineStore } from 'pinia'

// make the user store here
export const useUserStore = defineStore('user', {
  // the state of the store, gonna be used to hold the username and token of the user
  state: () => ({token: localStorage.getItem('storedusertoken') || null,username: localStorage.getItem('storedusername') || null,}),
  getters: {hasloggedin: (state) => !!state.token,}, // uses the fact that if a user is logged they have a token to detect if a user is logged in
  
  actions: {
    loguserin(token, username) // sets up the store when a user logs in
    {
      // get the token and username from the request made at login
      this.token = token 
      this.username = username

      // set these to local storage for persistence
      localStorage.setItem('storedusertoken', token)
      localStorage.setItem('storedusername', username)
    },

    // resets the store when a user logs out
    logoutuser()
    {
      // nullify users token and username
      this.token = null
      this.username = null

      // resets the local storage too 
      localStorage.removeItem('storedusertoken')
      localStorage.removeItem('storedusername')
    },
  },
})
