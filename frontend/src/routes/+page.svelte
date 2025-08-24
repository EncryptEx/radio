<script lang="ts">
  import { onMount } from "svelte";

  let songTitle: string = "Loading...";
  let songArtist: string = "Loading...";
  let songsAvailable: string[] = [];

  onMount(async () => {
    try {
      // Fetch data from the backend API.
      // This assumes your SvelteKit dev server proxies requests to the backend.
      const response = await fetch("http://127.0.0.1:5000/now-playing");
      if (response.ok) {
        const data = await response.json();
        songTitle = data.title || "Title not available";
        songArtist = data.artist || "Artist not available";
      } else {
        songTitle = "Error fetching song info.";
        songArtist = "Error fetching artist info.";
      }
    } catch (error) {
      console.error("Failed to fetch now playing data:", error);
      songTitle = "Could not connect to the server.";
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/songsAvailable");
      if (response.ok) {
        const data = await response.json();
        songsAvailable = data.musicfiles || [];
      } else {
        songsAvailable = [];
      }
    } catch (error) {
      console.error("Failed to fetch songs data:", error);
      songsAvailable = [];
    }
  });
</script>

<div class="bg-gray-900 py-16 sm:py-24">
  <div class="mx-auto max-w-2xl px-6 lg:max-w-7xl lg:px-8">
    <div class="flex">
      <div class="flex-1 w-48 mx-12 p-4 bg-gray-800 rounded-lg h-140">
        <img src="/img/synthwave.png" alt="Synthwave" class="rounded-lg" />
        <div class="rounded-full">
          <div class="justify-center">
            <p
              class="text-white dark:text-[#FAF9EF] text-lg mt-2"
              id="songname"
            >
              {songTitle}
            </p>
            <p
              class="text-white dark:text-[#FAF9EF] text-md"
              id="artistname"
            >
              {songArtist}
            </p>
            <button
              class="cursor-pointer mx-auto mt-2 w-24 h-24 rounded-full bg-white border shadow-xl flex items-center justify-center dark:bg-[#3E6990] bg-[#E9E3B4]"
              aria-label="Play"
            >
              <svg
                id="play-icon"
                class="ml-[10px]"
                width="31"
                height="37"
                viewBox="0 0 31 37"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M29.6901 16.6608L4.00209 0.747111C2.12875 -0.476923 0.599998 0.421814 0.599998 2.75545V33.643C0.599998 35.9728 2.12747 36.8805 4.00209 35.6514L29.6901 19.7402C29.6901 19.7402 30.6043 19.0973 30.6043 18.2012C30.6043 17.3024 29.6901 16.6608 29.6901 16.6608Z"
                  class="fill-[#3E6990] dark:fill-[#FAF9EF]"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="flex-2 w-96 px-12">
        <h2
          class="text-white dark:text-[#FAF9EF] text-3xl font-extrabold tracking-tight sm:text-4xl"
        >
          Songs Available
        </h2>
        <table class="mt-4 w-full text-left border-collapse">
          <thead>
        <tr>
          <th class="text-white dark:text-[#FAF9EF] text-lg border-b pb-2"> </th>
        </tr>
          </thead>
          <tbody>
        {#each songsAvailable as song}
            {#if song.match(/^[^"'＂]+["'＂](.*?)["'＂]\s+by\s+([^[]+)/i)}
            {@const match = song.match(/^[^"＂']+["＂'](.*?)["＂']\s+by\s+([^[]+)/i)}
            <tr>
              <td class="text-white dark:text-[#FAF9EF] py-2 border-b">
                <span class="font-bold">{match[1]}</span> <span class="italic">by {match[2]}</span>
              </td>
            </tr>
          {:else}
            <tr>
              <td class="text-white dark:text-[#FAF9EF] py-2 border-b">{song}</td>
            </tr>
          {/if}
        {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
</div>
