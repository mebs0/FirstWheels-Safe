<template>
  <h1 class=" text-center mb-4">My Garage</h1>
  <!-- This section is used to show the user their garage -->

  <!-- message telling the user there is no cars in their garage -->
  <div v-if="savedgaragecars.length==0" class=" alert alert-warning  text-center mb-4">No Cars In Garage! Press 'Save To Garage' When Searching A car</div>

  <ul class="list-group">
    <!-- going through all the cars in the garage and putting them into a table CRUD view -->
    <li v-for="car in savedgaragecars" :key="car.registration_number" class="list-group-item d-flex justify-content-between align-items-center" id="tablestyling">
      {{ car.registration_number }}
      <div>
        <!-- button to view a car -->
        <button class="btn btn-sm btn-outline-primary me-2" @click="garagelookup(car.registration_number)">View</button>
        <!-- button to remove a car -->
        <button class="btn btn-sm btn-outline-danger" @click="garagecarremove(car.registration_number)"> Remove </button>
      </div>
    </li>
  </ul>
  <p class="mt-3 alert alert-info ">Here Is Where Your Stored Cars Are Located Press View To Look Up The Corresponding Saved Car, Or Remove To Delete A Saved Car</p>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'


export default {
  // gets the user store info
  setup() { const loggedinuser = useUserStore(); return { loggedinuser } },
  // initialises a array to hold the garage items
  data() { return {savedgaragecars: [],}},
  async mounted() // at start get the users garage
  {
    try
    { // requests the users garage using the garage api endpoint, passing user info
      const getgaragecars = await axios.get('/vehicle/garage/', {headers: {Authorization: "Token "+this.loggedinuser.token},})
      this.savedgaragecars = getgaragecars.data
    } 
    catch (garageerror) {} // error catching
  },

  methods: {
    // view a garage vehicles info
    async garagelookup(selectedcarreg) // passes the reg that you want to lookup
    {
      try {
        // gets the results of the garage vehicle info and pushes it to the lookup form
        const lookupgaragecar = await axios.post('/vehicle/lookup/', {registrationNumber: selectedcarreg,})
        this.$router.push({ path: '/result', state: { vehicle: lookupgaragecar.data } })
      } 
      catch (garageerror) {} // error catching
    },
    
    // method to remove a vehicle from the garage
    async garagecarremove(selectedcarreg)
    {
      try
      { // sends a delete request to the garage endpoint passing over the user info and vehicle to remove
        await axios.delete('/vehicle/garage/', { headers: {Authorization: "Token "+this.loggedinuser.token}, data: { registration_number: selectedcarreg } })
      } 
      catch (garageerror) {} // error catching
      window.location.reload() // page refresh to update the garage items (vue reactivity doesnt work well in static mode)
    },
  },
}
</script>

<style>
#tablestyling
{
  /* styling for the garage table */
  background-color: #1f1f1f;
  color: #f8f9fa;
  border: 1px solid #444;
}
</style>