defmodule Main do
  def run do
    IO.puts("started the elixir node")

    # start the named process :hello on this node
    {:ok, _} = Hello.start_link()

    Process.sleep(20_000)
    IO.puts("stopped the elixir node")
  end
end

defmodule Hello do
  use GenServer

  # evaluated at script compile time
  @python_nodes (System.get_env("PYTHON_NODES") || "py@127.0.0.1") |> String.split(",") |> Enum.map(&String.to_atom/1)

  ## API
  def start_link(), do: GenServer.start_link(__MODULE__, 1)

  ## Callbacks
  @impl true
  def init(initial_count) do
    IO.puts("PYTHON_NODES=#{inspect(@python_nodes)}")
    :erlang.register(:hello, self())
    schedule_tick()
    {:ok, %{count: initial_count}}
  end

  # handle incoming messages sent from python
  @impl true
  def handle_info({:hello_from_python, python_pid, python_node, count}, state) do
    IO.puts("received :hello_from_python ##{count} from #{inspect(python_pid)} @ #{python_node}")
    {:noreply, state}
  end

  # handle scheduled tick messages
  @impl true
  def handle_info(:tick, %{count: count} = state) do
    # send a message to python
    send({:my_process, Enum.random(@python_nodes)}, {:hello_from_elixir, count, self()})
    schedule_tick()
    {:noreply, %{state | count: count + 1}}
  end

  defp schedule_tick() do
    Process.send_after(self(), :tick, 1000)
  end
end

Main.run()
