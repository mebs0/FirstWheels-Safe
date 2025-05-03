<template>
<div class = 'mb-4'>
  <!--This page is what will show the users checklist for when pre purchasing-->
  
  <h1 class="text-center mb-4 mt-1">Car Pre-Buy Checklist</h1>

  <div v-if="garage.length>0" class="form-group mb-4">
    <!-- This will make sure that there is cars in the garage before showing you a car to select -->
    <label for="carSelect" class="form-label"><strong>Select a Saved Car:</strong></label>
    <!-- This is the garage selection, as soon as a car is selected it will do the checklist logic -->
    <select v-model="carfromgarage" @change="checkliston" id="carSelect" class="form-select">
      <option disabled value="">Choose A Car From Garage</option>
      <!-- Loopa through all the cars in the garage -->
      <option v-for="carchecked in garage" :key="carchecked.registration_number" :value="carchecked.registration_number">{{carchecked.registration_number}}</option>
    </select>
  </div>
  <!-- 2 messages, one will give a notif popup if there is no cars in the garage, and
    the other will give a notif if a car isnt chosen from the garage selector -->
  <div v-if="garage.length==0" class=" alert alert-warning  text-center mb-4">No Cars In Garage! Press 'Save To Garage' When Searching A car</div>
  <div v-if="carfromgarage.length==0" class=" alert alert-info  text-center mb-4">Select A Car From Your Garage And Perform A 30 Point Check,Tick The Boxes If That Fault Is Not Present, After Finishing Use These Found Faults To Make A Decision To Whether You Should Buy The Car!</div>

  <div v-if="carfromgarage" class="alert border-info text-center mb-4">
    <!-- This section displays a box with the issues, divided into critical non critical and total issues -->
    <strong>Total Issues: </strong>{{totalIssues}} <div></div>
    <strong>Majour: </strong>{{criticalIssues}}
    <strong>| Minor: </strong>{{nonCriticalIssues}}
  </div>

  <!-- If we have a car selected then it will show the checklist here -->
  <div v-if="carfromgarage">
    <div v-for="(listoption, cararea) in checkliststore" :key="cararea" class="mb-3 border rounded">
      <!-- Shows the label of the checklist group for example engine -->
      <h5 class=" text-light p-2 fw-semibold">{{cararea}}</h5>
      <div class="row row-cols-1 row-cols-md-2">
        <!-- Ouput the actual checklist here, depending on if its critical or not then a color code is added -->
        <div v-for="optionentry in listoption" :key="optionentry.checkitem" class="form-check mb-2 col offset-1"
          :class="{'good': checklist[optionentry.checkitem] === true,'bad': checklist[optionentry.checkitem] === false && optionentry.critical,'pot': checklist[optionentry.checkitem] === false && !optionentry.critical}">
          <input type="checkbox" class="form-check-input" v-model="checklist[optionentry.checkitem]"/>
          <label class="form-check-label" :for="`${cararea}-${optionentry.checkitem}`">{{optionentry.checkitem}}</label>
        </div>
      </div>
    </div>
<!-- button to save the checklist -->
    <button @click="savechecklist" class="btn btn-dark w-100 mb-4 "> Save Checklist</button>

  </div>
</div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  setup()
  {
  // gets the logged in user from the user store and returns the info to be used
    const loggedinuser = useUserStore()
    return { loggedinuser }
  },
  data() {
    return {
      carfromgarage: '', garage: [], checklist: {},
      // this is where we have the checkliststore, essentailly this is a list of all the categories that 
      // we have in the checklist, due to the database structure we can easily add more items here without 
      // breaking the database, it will simply update the database beacuse its a json object saved to the db
      checkliststore: {
        "Engine":
        [
          {checkitem: "Engine Oil Between Min and Max", critical: true},
          {checkitem: "Coolant Between Min And Max", critical: true},
          {checkitem: "Engine Bay Dry (No Shiny Pools Of Liquid)", critical: true},
          {checkitem: "Engine Start Smoothly (No Clunks / Grinds)", critical: true},
          {checkitem: "Engine Idles Smoothly (1k - 1.5k Rpm)", critical: false},
        ],
        "Brakes":
        [
          {checkitem: "Brake Pedal Is Firm", critical: true},
          {checkitem: "No ABS / Brake Lights On The Dash", critical: true},
          {checkitem: "Brake Fluid Between Min and Max", critical: true},
          {checkitem: "Brakes Sound Good, No Screeching Sound", critical: false}
        ],
        "Lights":
        [
          {checkitem: "Lights Are All Working", critical: true},
        ],
        "Tyres & Suspension":
        [
          {checkitem: "Tyre Tread Above 1.6mm", critical: true},
          {checkitem: "Car Bounces up Only Once If Pushed", critical: false},
        ],
        "Interior":
        [
          {checkitem: "Seats Are In Good Condition", critical: false},
          {checkitem: "No Warning Lights Popping Up", critical: true},
          {checkitem: "AC Is Working", critical: false},
          {checkitem: "Heating Is Working", critical: false},
          {checkitem: "Windows All Go Up And Down", critical: false},
          {checkitem: "The Horn Works And Is Loud", critical: true}
        ],
        "Exterior":
        [
          {checkitem: "No Majour Dents, Scratches", critical: false},
          {checkitem: "Colour Of Paint Is Not Faded", critical: true}
        ],
        "Paperwork":
        [
          {checkitem: "Have The VC5 Logbook", critical: true},
          {checkitem: "Full Service History", critical: false},
          {checkitem: "Valid MOT (Check Lookup Page)", critical: true},
        ],
        "Test Drive":
        [
          {checkitem: "Car Moves Straight With The Wheel", critical: true},
          {checkitem: "Gear Changes Are Smooth, No Clunks", critical: true},
          {checkitem: "No Lous Noises Coming From The Car", critical: true}
        ],
        "Electrical":
        [
          {checkitem: "Infotainment Screen Working", critical: false},
          {checkitem: "No Green Buildup On Battery Terminals", critical: false},
          {checkitem: "Car Alarm Goes Off When Tested", critical: false}
        ]
      }
    }
  },
  computed: {
    totalIssues() {
      // a helper method which just goes through all the checklist items, checking if they are selected or are an issue and returns the total
      let amountofissues = 0;
      const categories = Object.keys(this.checkliststore);
      for (let category of categories) 
      {
        const items = this.checkliststore[category];
        // goes through the checklist items
        for (let item of items) 
        {
          const isChecked = this.checklist[item.checkitem];
          if (!isChecked) amountofissues++;
        }
      }

      return amountofissues;
    },
    criticalIssues() {
      // this is another method just like above but it checks for all critical issue by checklis the critical value within the store

      let issuesfound = 0;
      const allcategories = Object.keys(this.checkliststore);
      for (let singlecategory of allcategories) {
        const itemspercategory = this.checkliststore[singlecategory];
        // goes through the checklist items
        for (let singleitems of itemspercategory)
        {
          const isChecked = this.checklist[singleitems.checkitem];
          if (singleitems.critical && !isChecked) issuesfound++;
        }
      }
      return issuesfound;
    },
    // does total issues - critical issues which gets the non critical issues that is retured
    nonCriticalIssues() {return this.totalIssues - this.criticalIssues;}
  },

  methods: {
    async getgarage()
    {
      
      try // this is where we get the vehicles from the garage using the django garage api
      {
        const loadgarageattempt = await axios.get("/vehicle/garage/", { headers: {Authorization: "Token "+this.loggedinuser.token } }) // pass user info
        this.garage = loadgarageattempt.data
      }
      catch (garageerror) {alert('Could not load garage.')}
    },
    async checkliston()
    {
      try
      {
        const applychecklist = {} // make a empty array
        // get the checklist from django api
        const loadchecklistattempt = await axios.get('/vehicle/checklists/', { headers: {Authorization: "Token "+this.loggedinuser.token } }) // pass user info
        // goes through the users checklist and finds the one that matches the car reg they chose
        const match = loadchecklistattempt.data.find(currentval => currentval.registration_number === this.carfromgarage)
        for (const categories in this.checkliststore)
        {
          for (const val of this.checkliststore[categories])
          { 
            const valfromdb = match?.checklist?.[val.checkitem]
            applychecklist[val.checkitem] = valfromdb === true
          }
        }

        this.checklist = applychecklist
      }
      catch (checklisterror) {alert('Could not loadup checklist.')}
    },

    // where we save the checklist to the database using the checklsit api in POST mode
    async savechecklist()
    { 
      if (!this.carfromgarage) return alert('Please select a car.')
      try // send to the api checcklist with the reg number, checklist object and user token
      {
        await axios.post('/vehicle/checklists/',{registration_number: this.carfromgarage,checklist: this.checklist},{ headers: { Authorization: "Token "+this.loggedinuser.token } })
        alert('Checklist been saved!')
      }
      catch (checklisterror) {alert('Error when sabing checklist.')}
    }
  },
  created() {this.getgarage()}
}
</script>
<!-- These are the styles that we use to colour code the checklist items -->
<style scoped>
.bad{color: #dc3545 !important;}
.pot{color: #ffc107 !important;}
.good{color: #28a745 !important;}
</style>