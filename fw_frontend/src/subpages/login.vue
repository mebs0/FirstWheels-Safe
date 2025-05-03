<template>
  <form @submit.prevent="needsaccount ? createaccount() : loginaccount()">
    <!-- depending on if we are signing up or logging in link to the respective method -->
    <h4 class="text-center mb-3">{{ needsaccount ? 'Sign Up' : 'Log In' }}</h4>
    <!-- depending on if we are signing up or loggin in dispay the correct header -->

    <!--  our form input are here -->
    <input v-model="userusername" placeholder="Username" class="form-control mb-3" required />
    <input v-model="userpassword" placeholder="Password" type="password" class="form-control mb-2" required />
    <!--  verify password if in signup mode -->
    <input v-if ="needsaccount" v-model="userpassword2" placeholder="Confirm Password" type="password" class="form-control mb-3" required />

    <!-- button to submit form -->
    <button type="submit" class="btn btn-dark w-100">
      {{ needsaccount ? 'Sign Up' : 'Log In' }}
    </button>

    <div class="text-center mt-3">
      <!--  text at the bottom which switches between signup and login -->
      <small>
        {{ needsaccount ? 'Have an Account?' : 'Need an account?' }}
        <a href="#" @click.prevent="needsaccount = !needsaccount" class="text-info">
          {{ needsaccount ? 'Log In' : 'Sign Up' }}
        </a>
      </small>
    </div>
    <!-- any errors are displayed here -->
    <div v-if="founderros" class="text-center alert alert-danger mt-5">{{founderros}}</div>
  </form>
</template>


<script>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export default {
  // uses the user store for storing credentials
  setup()
  {
    const loggedinuser = useUserStore()
    const menubar = useRouter()
    return { loggedinuser, menubar }
  },
  data()
  {
    return {
      // holds all the fields that the form uses and the boolean on what mode we are in
      needsaccount: false,
      userusername: '',
      userpassword: '',
      userpassword2: '',
      founderros: '',
    }
  },
  methods: {
    // method to login a user
    async loginaccount()
    {
      this.founderros = '' // resets any errors
      try
      {
        // posts the login form to the login api endpoint 
        const loginattempt = await fetch('/user/login/',{method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: this.userusername, password: this.userpassword, password2: this.password2 }),})
        const loginattemptresponce = await loginattempt.json()
        if (!loginattempt.ok)
        {
          // if the login is not okay output the error and reset fields
          this.founderros = loginattemptresponce.loginerror
          this.userusername = ''
          this.userpassword = ''
          return
        }

        // log the user in (in the user store)
        this.loggedinuser.loguserin(loginattemptresponce.token, loginattemptresponce.username)
        this.menubar.push('/')
      }
      catch (loginerrorr){} // error checking

    },

    async createaccount() // method for signing in a user
    {
      this.founderros = '' // resets the errors
      try
      {
        // send the details to the signup api endpoint
        const singupattempt = await fetch('/user/signup/',
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({username: this.userusername, password: this.userpassword, password2: this.userpassword2}),
        })
        const singupattemptresponce = await singupattempt.json()
        // if signup fails display the error and also reset the form
        if (!singupattempt.ok)
        {
          this.founderros = singupattemptresponce.signuperror
          this.userusername = ''
          this.userpassword = ''
          this.userpassword2 = ''
          return
        }
        // if okay log the user in (user store code)
        this.loggedinuser.loguserin(singupattemptresponce.token, singupattemptresponce.username)
        this.menubar.push('/')
      }
      catch (singuperrorr) {} // error checking

    },
  },
}
</script>


