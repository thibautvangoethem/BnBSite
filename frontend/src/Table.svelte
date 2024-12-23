<script>
  import { onMount } from 'svelte';

  let data = [];
  let loading = false;
  let error = null;

  async function fetchData() {
    loading = true;
    error = null;
    try {
      const response = await fetch('http://localhost:8000/testGet');

      if (!response.ok) {
        throw new Error(`Failed to fetch: ${response.status}`);
      }

      data = await response.json();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  // Ensure the fetch is triggered when the component is mounted
  onMount(() => {
    fetchData();
  });
</script>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  th {
    background-color: #f4f4f4;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  .loading {
    margin-top: 10px;
  }
</style>

<!-- UI -->
<div>
  <h1>API Data Visualization</h1>

  <!-- Show a loading spinner while fetching data -->
  {#if loading}
    <p class="loading">Loading data...</p>
  {/if}

  <!-- Show an error message if the fetch fails -->
  {#if error}
    <p class="error">Error: {error}</p>
  {/if}

  <!-- Show the data in a table if available -->
  {#if !loading && data.length > 0}
    <table>
      <thead>
        <tr>
          <!-- Adjust columns based on your API data structure -->
          {#each Object.keys(data[0]) as key}
            <th>{key}</th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each data as row}
          <tr>
            {#each Object.values(row) as cell}
              <td>{cell}</td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>