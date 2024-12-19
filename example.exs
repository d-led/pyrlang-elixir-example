defmodule Main do
  def run do
    {:ok, _} = Hello.start_link()

    IO.puts("started the elixir node")
    Process.sleep(20_000)
    IO.puts("stopped the elixir node")
  end
end

defmodule Hello do
  use GenServer

  ## API
  def start_link(), do: GenServer.start_link(__MODULE__, 1)

  ## Callbacks
  @impl true
  def init(count) do
    :erlang.register(:hello, self())
    schedule_tick()
    {:ok, %{count: count}}
  end

  # handle incoming messages sent from python
  @impl true
  def handle_info({:hello_from_python,python_pid, count}, state) do
    IO.puts("received :hello_from_python ##{count} from pid(#{inspect(python_pid)}})}")
    {:noreply, state}
  end

  @impl true
  def handle_info(:tick, %{count: count} = state) do
    # send a message to python
    send({:my_process, :'py@127.0.0.1'}, {:hello_from_elixir, count})
    schedule_tick()
    {:noreply, %{state | count: count + 1}}
  end

  defp schedule_tick() do
    delay = round(1000)
    Process.send_after(self(), :tick, delay)
  end
end

Main.run()
