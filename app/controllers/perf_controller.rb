class PerfController < ApplicationController
  include ActionController::Live

  def health
    render json: { ok: true, ts: Time.now.to_f }
  end

  # Simulate I/O wait (not CPU). Param s = seconds.
  def slow
    delay = params.fetch(:s, "0.2").to_f
    random_guid = SecureRandom.uuid
    sleep delay
    render json: { ok: true, slept: delay, guid: random_guid }
  end

  # Chunked stream / simple SSE-ish output to visualize multiplexing
  def stream
    response.headers['Content-Type'] = 'text/event-stream'
    begin
      10.times do |i|
        response.stream.write "data: tick #{i} @ #{Time.now.to_f}\n\n"
        sleep 0.25
      end
    ensure
      response.stream.close
    end
  end
end
