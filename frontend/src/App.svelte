<script>
  // Define a function to handle the button click
  const backendUrl = import.meta.env.VITE_BACKEND_URL;

  async function fetchData() {
    try {
      const response = await fetch(backendUrl+'/testAdd', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json(); // Parse the JSON response
      console.log(data); // Do something with the data (e.g., update the UI)
    } catch (error) {
      console.error('Error fetching data:', error);
      alert('Error fetching data! Check the console for more details.');
    }
  }
</script>


<button on:click={fetchData}>Call REST Endpoint</button>


<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
