<template>
  <div class="container text-center text-light">
    <h1 class="mb-4">Welcome To First Wheels</h1>
    <!--This code is what the user sees when looking up a car registration-->

    <!-- The input box for manual input-->
    <input v-model="scannedreg" placeholder="EG00 REG" class="regstyle  mt-4 mb-3"/>

    <button @click="textreglookup" class="btn btn-dark w-100 mb-2">Lookup</button>
    <!--Button to start the anpr mode, goes to the anpron method-->
    <button @click="anpron" class="btn btn-primary w-100 mb-3">ANPR Mode</button>
    <!-- Video element thats used to link the mobile camera to the system-->
    <video v-if="livescanning" ref="video" autoplay class="w-100 mb-3"></video>
    <!--holds error messages or notifs-->
    <div v-if="message" class="alert alert-info">{{message}}</div>
    <div v-if="regissue" class="alert alert-danger">{{regissue}}</div>
    <p class="mt-3 alert alert-info ">Here Is Where You Can Lookup A Car, Enter The Reg Above Or Select ANPR Mode To Live Scan A Car </p>
    <p class="mt-3 alert alert-warning ">Remember To Log In To Access Your Garage, And Pre Buy Checklist!! </p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    // this is where we hold the data used for scanning the reg
    // includes the scanned plate which is returned by django
    // any issues and also helpers to tell the system what state its in
    return{
      scannedreg: '',
      regissue: '',
      message: '',
      livescanning: false,
      livescancount: null,
    }
  },

  methods: {
    async textreglookup() // this is the method that does text based lookup
    {
      // empty value handling
      if (!this.scannedreg) { this.regissue = 'You Did Not Enter A Reg!' 
      return}

      this.regissue = '' // resets the errors incase we decide to rescan
      try { // sends the plate to django and sends the result to the inforesult page using vue router
          const findreg = await axios.post('/vehicle/lookup/', { registrationNumber: this.scannedreg,})
          this.$router.push({path: '/result', state: { vehicle: findreg.data },})} 
      catch (lookuperror) {this.regissue = 'Registration Not Found!'} // error handling
    },

    // this method is what does the scanning of the reg plate
    async anpron() 
    {
      this.regissue = '' // reset the error messages
      this.livescanning = true // tell the system we are live scanning (enables video element)

      try 
      { // here we start the camera stream and set it to use the rear camera
        const browserstream = await navigator.mediaDevices.getUserMedia({ video:{facingMode:{exact: "environment"}}})
        this.$refs.video.srcObject = browserstream


        this.livescancount = setInterval(async () => {
          const videostream = this.$refs.video // links the stream to a variable we can use

          // makes a canvas panel for the system to write the image to
          const campanel = document.createElement('canvas')
          // make the panel the height and width of the camera
          campanel.width = videostream.videoWidth
          campanel.height = videostream.videoHeight
          // starts a drawer to use for adding image to the panel 
          const drawer = campanel.getContext('2d')
          // draws a the image to the panel
          drawer.drawImage(videostream, 0, 0, campanel.width, campanel.height)

          // converts the image to a blob and adds it to a formdata element
          const frameblob = await new Promise(resolve => campanel.toBlob(resolve, 'image/jpeg'))
          const framepayload = new FormData()
          framepayload.append('imagetocheck', frameblob)

          try 
          {// attempts to send the data to the anpr api
            const findreg = await axios.post('/vehicle/scananpr/', framepayload)
            if (findreg.data.gotplate) {
              // if we get the plate, tell the user this and add it to the input box
              this.scannedreg = findreg.data.plate
              this.message = `Plate found: ${findreg.data.plate}`
              // stop camera link 
              this.anproff()
            }
          } 
          catch (camerror) {console.error('Issue Scanning Plate:', camerror)} // error checking

        },450)
      } 
      catch (camerror)  // if user doesnt accept camera usage then error is shown
      {
        this.regissue = 'Not Able To Turn On Camera, Did You Allow It?'
        this.livescanning = false
      }
    },

    anproff() // switches off anpr 
    { // tells the forms the anpr link is off
      if (!this.livescanning) return
      this.livescanning = false
      if (this.livescancount) clearInterval(this.livescancount)
      // swiches the browser camlink off
      const browserstream = this.$refs.video?.srcObject
      if (browserstream) browserstream.getTracks().forEach(track => track.stop())
    },

  },

  beforeUnmount() {this.anproff()}, // if we jump off the page suddenly switch off anpr
}
</script>

<style>
.regstyle
{
/* this is the number plate looking input box styling */
  background-color: yellow;
  text-align: center;
  font-weight: 900;
  font-size: x-large;
  border: 1px solid black;
  border-radius: 4px;
  padding: 0.7rem 1rem;
  width: 95%;
  margin: 0 auto;
}

.regstyle::placeholder
/* this is the text within the number plate box */
{
  color: black;
  opacity: 50%;
}

</style>

