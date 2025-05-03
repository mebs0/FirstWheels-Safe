<template>
  <div v-if="!correctcar" class="d-flex justify-content-center">
    <!-- this is the box that asks the user if the details of the car are correct -->
    <div class="dark-card border border-secondary p-4 text-center">
      <p class="mb-3 fs-2">Ensure These Details Look Right</p>
      <!-- diplays the make model and colour of the car for the user to double check -->
      <p class="fs-3 fw-bold">{{vehicle.make}} {{vehicle.model}} IN {{vehicle.colour}}</p>
      <!-- buttons to confirm its correct or not -->
      <button class="btn btn-success me-2" @click="correctcar = true">Yes</button>
      <!-- uses router history to go back -->
      <button class="btn btn-danger" @click="$router.push('/')">No</button>
    </div>
  </div>

  <div v-if="correctcar" class="container pb-5 mt-4 text-light">
    <!-- if the vehicle is identified we show the results -->
    <h4 class="text-center fw-bold mb-3">{{vehicle.make}} {{vehicle.model}}</h4>
    <!-- simple tabs to go between mot, technical and the overview -->
    <ul class="nav nav-tabs mb-4 justify-content-center menubar">
      <li class="nav-item"><a class="nav-link" :class="{ active: currentsection === 'review' }" @click="currentsection = 'review'">Car Review</a></li>
      <li class="nav-item"><a class="nav-link" :class="{ active: currentsection === 'tech' }" @click="currentsection = 'tech'">Technical Info</a></li>
      <li class="nav-item"><a class="nav-link" :class="{ active: currentsection === 'mot' }" @click="currentsection = 'mot'">MOT</a></li>
    </ul>
    <!-- button to save the car to the garage -->
    <button class="btn btn-dark w-100 mb-4" @click="saveToGarage">Add To My Garage</button>
    <!--  if in the review section then we show suitability score -->
    <div v-if="currentsection === 'review'">
      <div class="d-flex justify-content-between align-items-center mb-2">
        <div class="text-center">
          <!-- get the vehicle score and a description e.g. 70/100 This vehicle is a good choice -->
          <div class="fs-1 fw-bold mb-1" :class="calcscore(vehicle.score)">{{calcscoredesc(vehicle.score)}}</div>
          <div class="text large">SCORE: {{vehicle.score}}/100</div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col mb-3">
          <div class="card h-100 dark-card">
            <!-- this section loops through all the pros we get from django and displays -->
            <div class="card-header bg-success">Pros</div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item dark-card" v-for="(foundpros, i) in vehicle.advice?.selectedvehiclepros" :key="'pro-' + i">{{foundpros}}</li>
            </ul>
          </div>
        </div>

        <div class="col-md-6 mb-4">
          <div class="card h-100 dark-card">
            <!-- this loops through all the cons we get from django and displays -->
            <div class="card-header bg-danger">Cons</div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item dark-card" v-for="(foundcons, i) in vehicle.advice?.selectedvehiclecons" :key="'con-' + i">{{foundcons}}</li>
            </ul>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card h-100 dark-card">
            <!-- this goes through all the tips we get from django and displays -->
            <div class="card-header bg-info">Tips</div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item dark-card" v-for="(foundtips, i) in vehicle.advice?.selectedvehicletips" :key="'tips-' + i">{{foundtips}}</li>
            </ul>
          </div>
        </div>

      </div>
    </div>

    <div v-else-if="currentsection === 'tech'">
      <!-- we output the technical details here by refrencing the json of DVLA VES and DVLA MOT -->
      <ul class="list-group mb-2">
        <li class="list-group-item dark-card"><strong>Make:</strong> {{vehicle.make}}</li>
        <li class="list-group-item dark-card"><strong>Model:</strong> {{vehicle.model}}</li>
        <li class="list-group-item dark-card"><strong>Tax Status:</strong> {{vehicle.taxStatus}}</li>
        <li class="list-group-item dark-card"><strong>Tax Due:</strong> {{vehicle.taxDueDate}}</li>
        <li class="list-group-item dark-card"><strong>MOT Status:</strong> {{vehicle.motStatus}}</li>
        <li class="list-group-item dark-card"><strong>Engine Capacity:</strong> {{vehicle.engineCapacity}} cc</li>
        <li class="list-group-item dark-card"><strong>CO₂ Emissions:</strong> {{vehicle.co2Emissions}}</li>
        <li class="list-group-item dark-card"><strong>Fuel Type:</strong> {{vehicle.fuelType}}</li>
        <li class="list-group-item dark-card"><strong>Colour:</strong> {{vehicle.colour}}</li>
        <li class="list-group-item dark-card"><strong>Last V5C Issued:</strong> {{vehicle.dateOfLastV5CIssued}}</li>
        <li class="list-group-item dark-card"><strong>MOT Expiry:</strong> {{vehicle.motExpiryDate}}</li>
        <li class="list-group-item dark-card"><strong>Wheelplan:</strong> {{vehicle.wheelplan}}</li>
        <li class="list-group-item dark-card"><strong>First Registered:</strong> {{vehicle.monthOfFirstRegistration}}</li>
        <li class="list-group-item dark-card"><strong>Outstanding Recalls:</strong> {{vehicle.hasOutstandingRecall}}</li>
      </ul>
    </div>

    <div v-else-if="currentsection === 'mot'">
      <!--  MOT Section of the screen -->

      <!-- loop through all the entries we get from the json and display -->
      <div v-for="test in vehicle.mot_data.motTests" :key="test.motTestNumber" class="card mb-3 dark-card border-secondary">
        <div class="card-body">
          <!-- slicking to get when the mot was completed -->
          <h6>MOT on {{test.completedDate.slice(0, 10)}} —
            <span :class="test.testResult === 'PASSED' ? 'text-success' : 'text-danger'">{{test.testResult}}</span>
          </h6>
          <!-- gets expiry date and odometer values from the json and assigns them to the box -->
          <p>Expiry: {{test.expiryDate}}</p>
          <p>Odometer: {{test.odometerValue}} {{test.odometerUnit}}</p>
          <!-- lists the defects here -->
          <div>
            <p><strong>Defects:</strong></p>
            <ul><li v-for="(defect, i) in test.defects" :key="i">{{defect.text}} ({{defect.type}})</li></ul>
          </div>
        </div>
      </div>
    </div>
    <!--  go back using router history -->
    <button class="btn btn-dark w-100 mb-4" @click="$router.push('/')">Back To Search</button>

  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  // get the user info and also get the json we got from the reg lookup form
  setup() {const loggedinuser = useUserStore(); return {loggedinuser}},
  data() { return { currentsection: 'review', vehicle: history.state?.vehicle, correctcar: false,} },
  methods:
  {
    calcscoredesc(carrating) 
    {
      // gets the description of a car rating based on score from 
      // data processing algorithm
      const intcarrating = parseInt(carrating)
      if (intcarrating <= 50) return 'This Car Is A Bad Choice'
      if (intcarrating <= 70) return 'This Car Is A Okay Choice'
      if (intcarrating <= 85) return 'This Car Is A Good Choice'
      return 'This Car Is A Great Choice'
    },
    calcscore(carrating)
    {
      // all this does it assign a color to the score we get
      // from the data processing algorithm
      const intcarrating = parseInt(carrating)
      if (intcarrating > 85) return 'text-success'
      if (intcarrating > 70) return 'text-info'
      if (intcarrating > 50) return 'text-warning'
      return 'text-danger'
    },

    async saveToGarage() // method to save to a garage
    {
      // get the reg from the variable
      const reg = this.vehicle.registrationNumber

      // send the reg and user info to the garage api
      try {const savetogarage = await axios.post('/vehicle/garage/',{ registration_number: reg },
      {headers: {Authorization: "Token "+this.loggedinuser.token},})
      // if added tell the user this or tell them its already added
        alert(savetogarage.data.status === 'Added' ? 'Saved to garage' : 'Already in garage')
      } 
      // error handling
      catch (garageerror) {alert('Could not save to garage. Are you logged in?')}
    },
  },
}
</script>

<style scoped>
.menubar .nav-link
{
  /* style for the top menu bar mot,technical,review */
  background-color: #353b41;
  color: #aaa;
  border: 1px solid #555;
}
.menubar .nav-link.active
{
  /* styling for when we click a tab */
  background-color: #3f454a;
  color: white;
}

/* styling for the mot section boxes and the background cards */
.card,.card-header,.list-group-item,.dark-card {background-color: #1e1e1e;}
.dark-card {color: white;}
</style>


