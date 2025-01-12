<script>
  import App from './App.svelte';
  import Table from './Table.svelte';
  import Login from './Login.svelte';

  // Reactive variable for tracking the current route
  let currentRoute = 'home';

  // Route mapping: Map route names to components
  const routes = {
    home: App,
    table: Table,
    login: Login,
  };

  // Get the current page's component
  $: CurrentPage = routes[currentRoute];
</script>

<style>
  nav {
    margin-bottom: 20px;
  }
  nav a {
    margin-right: 10px;
    text-decoration: none;
    color: blue;
    cursor: pointer;
  }
  nav a.active {
    font-weight: bold;
    color: darkblue;
  }
</style>

<!-- Navigation -->
<nav>
  <a
    href="#"
    class:active={currentRoute === 'home'}
    on:click={() => currentRoute = 'home'}
  >
    Home
  </a>
  <a
    href="#"
    class:active={currentRoute === 'table'}
    on:click={() => currentRoute = 'table'}
  >
    Table
  </a>
  <a
    href="#"
    class:active={currentRoute === 'login'}
    on:click={() => currentRoute = 'login'}
  >
    Login
  </a>
</nav>

<!-- Render the current page -->
<svelte:component this={CurrentPage} />